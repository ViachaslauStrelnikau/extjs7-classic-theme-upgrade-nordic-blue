(function () {
    'use strict';
    // Fixture-only clock. Loaded before Ext; installed SDK and production JS are untouched.
    const NativeDate = window.Date;
    const epoch = NativeDate.parse('2026-10-23T09:00:00+03:00');
    function FixtureDate(...args) {
        if (!new.target) return new NativeDate(epoch).toString();
        return Reflect.construct(NativeDate, args.length ? args : [epoch], new.target);
    }
    Object.setPrototypeOf(FixtureDate, NativeDate);
    FixtureDate.prototype = NativeDate.prototype;
    // TaskRunner/HtmlEditor require elapsed time; anchor timers to the fixture epoch.
    // new Date() stays fixed for calendar/today values, while Date.now() advances.
    const timerStart = performance.now();
    FixtureDate.now = () => epoch + Math.floor(performance.now() - timerStart);
    window.Date = FixtureDate;
    window.labClock = {epoch, iso: '2026-10-23T06:00:00.000Z', timezone: 'Europe/Minsk'};
    // Observe trusted browser input before Ext's delegated event handlers can stop it.
    for (const eventName of ['mouseover','pointerdown','mousedown']) document.addEventListener(eventName, event => {
        const lab=window.themeLab;if(!lab||!event.isTrusted||!event.target.closest)return;
        const handled=lab.pendingActions.filter(a=>(a.kind==='mousedown'?['pointerdown','mousedown'].includes(eventName):eventName==='mouseover')&&event.target.closest(a.selector));
        if(!handled.length)return;
        lab.pendingActions=lab.pendingActions.filter(a=>!handled.includes(a));
        queueMicrotask(()=>lab.whenReady().catch(error=>{lab.errors.push(String(error));lab.status='ERROR';}));
    },true);
}());
