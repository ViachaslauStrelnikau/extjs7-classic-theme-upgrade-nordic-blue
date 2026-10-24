(async function () {
    'use strict';
    const params = new URLSearchParams(location.search);
    const theme = params.get('theme') || 'classic';
    const status = document.getElementById('lab-status');
    window.labBoot = {status: 'LOADING', theme, errors: []};
    function fail(error) {
        window.labBoot.status = 'ERROR';
        window.labBoot.errors.push(String(error));
        status.textContent = String(error);
        status.classList.add('lab-error');
    }
    window.addEventListener('error', e => { if (e.message) fail(e.message); });
    window.addEventListener('unhandledrejection', e => fail(e.reason));
    async function json(url) {
        const response = await fetch(url, {cache: 'no-store'});
        if (!response.ok) throw new Error('Profile/build unavailable: ' + url + ' (HTTP ' + response.status + ')');
        return response.json();
    }
    function load(url, type) {
        return new Promise((resolve, reject) => {
            const el = document.createElement(type === 'css' ? 'link' : 'script');
            if (type === 'css') { el.rel = 'stylesheet'; el.href = url; }
            else el.src = url;
            el.onload = resolve;
            el.onerror = () => reject(new Error('Failed to load ' + url));
            document.head.appendChild(el);
        });
    }
    try {
        const config = await json('profiles.json');
        const profile = config.profiles[theme];
        if (!profile) throw new Error('Unknown theme: ' + theme);
        const manifestUrl = new URL(profile.manifest, location.href);
        const manifest = await json(manifestUrl);
        if (manifest.verify) {
            const versionResponse=await fetch(new URL(manifest.verify.versionProperties,manifestUrl),{cache:'no-store'});
            const versionText=await versionResponse.text();
            const metadata=await json(new URL(manifest.verify.themePackage,manifestUrl));
            if (!versionResponse.ok || !versionText.includes('version.full='+config.sdkVersion) || metadata.sencha.name!==profile.requiredPackage) {
                throw new Error('Installed SDK proof does not match reference profile');
            }
        }
        if (manifest.toolkit !== 'classic' || !profile.allowedThemeNames.includes(manifest.theme)) {
            throw new Error('Wrong build theme/toolkit: ' + manifest.theme + '/' + manifest.toolkit);
        }
        const pkg = manifest.packages && manifest.packages[profile.requiredPackage];
        if (!pkg || !pkg.included || !manifest.packages.ext || manifest.packages.ext.version !== config.sdkVersion) {
            throw new Error('Build package/SDK mismatch; required ' + profile.requiredPackage + ' on ' + config.sdkVersion);
        }
        const styles = (manifest.css || []).filter(c => c.path && !c.remote);
        if (!styles.length) throw new Error('Build has no compiled CSS');
        await Promise.all(styles.map(c => load(new URL(c.path, manifestUrl).href, 'css')));
        window.labBoot.profile = {theme, manifestUrl: manifestUrl.href, package: profile.requiredPackage, sdk: config.sdkVersion, css: styles.map(c => new URL(c.path, manifestUrl).href)};
        await load(new URL(config.script, location.href).href, 'js');
        if (Ext.getVersion().version !== config.sdkVersion) throw new Error('Runtime SDK mismatch');
        await load(new URL('fixture.js', location.href).href, 'js');
    } catch (error) { fail(error); }
}());
