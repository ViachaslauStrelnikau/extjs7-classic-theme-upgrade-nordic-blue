"""Validate the separate, narrowly reviewed Nordic Soft Contrast child package."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "TestApp/packages/local/theme-nordic-blue-soft-contrast"
POLICY = json.loads((ROOT / "config/nordic-soft-contrast-policy.json").read_text(encoding="utf-8"))
errors = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Preserve the old paint review and require its approved rules exactly once.
base_review_path = ROOT / POLICY["decorativeReview"]
base_review = json.loads(base_review_path.read_text(encoding="utf-8"))
if sha(base_review_path) != POLICY["decorativeReviewSha256"]:
    errors.append("Changed TASK-053 decorative review")
if sha(ROOT / POLICY["approval"]) != POLICY["approvalSha256"]:
    errors.append("Changed TASK-053 approval")

# Motion is an explicit, exact-hash exception, not a general CSS/runtime allowlist.
motion_review_path = ROOT / POLICY["motionReview"]
motion_review = json.loads(motion_review_path.read_text(encoding="utf-8"))
if sha(motion_review_path) != POLICY["motionReviewSha256"]:
    errors.append("Changed TASK-054 motion review")
if sha(ROOT / motion_review["designApproval"]) != POLICY["motionApprovalSha256"]:
    errors.append("Changed TASK-054 user approval record")
if POLICY.get("runtimeOverrides") is not True or POLICY.get("reviewedRuntimeOverrides") != {motion_review["override"]: motion_review["overrideSha256"]}:
    errors.append("Runtime override policy is not the exact TASK-054 exception")

for relative, expected in POLICY["reviewedFiles"].items():
    path = ROOT / relative
    if not path.is_file() or sha(path) != expected:
        errors.append("Unreviewed source " + relative)

entry_path = PACKAGE / "sass/etc/all.scss"
if not entry_path.is_file() or entry_path.read_text(encoding="utf-8-sig").strip() != '@import "../src/Motion";':
    errors.append("Unexpected motion Sass entrypoint")

css_path = ROOT / motion_review["stylesheet"]
if not css_path.is_file() or sha(css_path) != motion_review["stylesheetSha256"]:
    errors.append("Changed TASK-054 motion stylesheet")
else:
    css = css_path.read_text(encoding="utf-8-sig")
    # Hash-binding already fixes the exact selectors/values. These assertions make
    # the reviewed intent legible and reject a malformed/mis-targeted artifact.
    required_css = [
        "animation: nb-softcontrast-fade-in 90ms ease-out",
        "animation: nb-softcontrast-float-in 70ms ease-out",
        "animation: nb-softcontrast-float-in 110ms ease-out",
        "animation: nb-softcontrast-float-in 100ms ease-out",
        "transition-duration: 120ms",
        "@media (prefers-reduced-motion: reduce)",
        "transition: none !important",
        "animation: none !important",
    ]
    for rule in required_css:
        if css.count(rule) != 1:
            errors.append("Missing/duplicate reviewed motion rule: " + rule)

# The one exact Ext override is theme-scoped and immutable by SHA. All other
# overrides/runtime JS remain prohibited.
allowed_overrides = {motion_review["override"]: motion_review["overrideSha256"]}
actual_overrides = {
    path.relative_to(ROOT).as_posix(): sha(path)
    for path in (PACKAGE / "overrides").rglob("*") if path.is_file()
}
if actual_overrides != allowed_overrides:
    errors.append("Unexpected or changed Ext override set")
override_path = ROOT / motion_review["override"]
if not override_path.is_file() or sha(override_path) != motion_review["overrideSha256"]:
    errors.append("Changed TASK-054 tree override")
else:
    override_text = override_path.read_text(encoding="utf-8-sig")
    for expected in [
        "override: 'Ext.tree.View'",
        "expandDuration: 125",
        "collapseDuration: 125",
        "prefers-reduced-motion: reduce",
        "this.animate = false",
    ]:
        if override_text.count(expected) != 1:
            errors.append("Missing/duplicate tree motion contract: " + expected)

all_js = {path.relative_to(ROOT).as_posix() for path in PACKAGE.rglob("*.js")}
if all_js != set(allowed_overrides):
    errors.append("Unexpected package runtime JavaScript")

for path in PACKAGE.rglob("*.scss"):
    relative = path.relative_to(ROOT).as_posix()
    source = path.read_text(encoding="utf-8-sig")
    if source.strip() and relative not in POLICY["reviewedFiles"]:
        errors.append("Extra Sass " + relative)
    if relative.endswith("/sass/src/Component.scss"):
        checked = source
        for block in base_review["rules"]:
            if checked.count(block) != 1:
                errors.append("Missing/duplicate exact TASK-053 decorative rule")
            checked = checked.replace(block, "")
        properties = set(re.findall(r"(?:^|[;{])\s*([a-z-]+)\s*:", checked))
        if properties - set(POLICY["approvedPaintProperties"]):
            errors.append("Non-paint property " + str(properties - set(POLICY["approvedPaintProperties"])))

for path in PACKAGE.rglob("*.scss"):
    if "/sass/var/" in path.as_posix():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if line.strip() and not line.strip().startswith("//") and not re.fullmatch(
                r"\$[a-z-]+: dynamic\(#[0-9A-Fa-f]{6}\);", line
            ):
                errors.append("Non-color variable " + line)

artwork_suffixes = {".png", ".gif", ".svg", ".woff", ".ttf"}
if any(path.is_file() and path.suffix.lower() in artwork_suffixes for path in (PACKAGE / "resources").rglob("*")):
    errors.append("Unapproved artwork/font")

package_text = (PACKAGE / "package.json").read_text(encoding="utf-8-sig")
package_text = re.sub(r'("(?:\\.|[^"\\])*")|/\*[\s\S]*?\*/|//[^\r\n]*', lambda match: match[1] or "", package_text)
metadata = json.loads(package_text)
if metadata["name"] != POLICY["theme"] or metadata["sencha"]["extend"] != POLICY["parent"] or metadata["sencha"]["toolkit"] != "classic":
    errors.append("Theme inheritance")
if metadata["sencha"]["version"] != motion_review["packageVersion"]:
    errors.append("Theme package version")

print(json.dumps({"status": "FAIL" if errors else "PASS", "theme": POLICY["theme"], "reviewedFiles": len(POLICY["reviewedFiles"]), "allowedOverrides": len(allowed_overrides), "errors": errors}, indent=2))
sys.exit(bool(errors))
