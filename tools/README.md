# Nordic Blue source policy

From the project root run `python tools/lint-nordic-blue.py --check-icon-candidates` (standard library only). The verified bundled Python command is in AGENTS.md. Use `--report <path>` to save JSON. The script reads files and returns exit 0 for PASS, 1 for policy violations; it does not build the application.

`config/nordic-blue-policy.json` binds 15 tokens, exact color assignments, Ext namespace paths, SDK hashes and reviewed package configuration. `config/nordic-blue-icons.json` binds approved 1x/2x bytes, original logical sheet size and sprite contracts. Candidate validation checks all known exports and masters; integration remains disabled until TASK-013. Arbitrary stylesheet rules, UI mixins, geometry overrides and runtime JS are rejected. Future component/asset exceptions require explicit evidence and narrow reviewed policy entries.

Evidence and the 33 positive/negative controls are in artifacts/nordic-blue/TASK-008. Do not run preparation/installation helpers from those evidence files as routine checks: they reproduce historical mutations, while this lint command is read-only.
