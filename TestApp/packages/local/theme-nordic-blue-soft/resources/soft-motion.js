/* Optional public-component listeners. No Ext override or prototype patch. */
(function(root){'use strict';
 if(root.NordicSoftMotion)return;
 var enabled=false,states=[],media=root.matchMedia?root.matchMedia('(prefers-reduced-motion: reduce)'):null;
 function reduced(){return !!(media&&media.matches);}
 function cancel(s){if(s.animation){s.animation.cancel();s.animation=null;}}
 function sync(){if(root.document.body)root.document.body.classList.toggle('nb-soft-motion',enabled);if(!enabled||reduced())states.forEach(cancel);}
 function enable(value){enabled=value!==false;sync();}
 function attach(component,options){
  if(!component||!component.on||!component.un)throw Error('Expected an Ext Component');
  var existing=states.filter(function(s){return s.component===component;})[0];if(existing)return existing.detach;
  var s={component:component,animation:null,element:null,elevation:false},opts=options||{};
  function render(){var el=component.getEl();if(!el)return;s.element=el.dom;
   /* Let callers request the new elevation through the documented shadow:false config. */
   if(opts.elevation===true&&component.shadow===false){el.addCls('nb-soft-float');s.elevation=true;}
  }
  function show(){cancel(s);if(!s.element)render();
   /* Preserve configured native animateTarget/custom component animations. */
   if(!enabled||reduced()||component.animateTarget||!s.element||!s.element.animate)return;
   var opacity=Number(root.getComputedStyle(s.element).opacity);if(!isFinite(opacity))opacity=1;
   var animation=s.element.animate([{opacity:opacity*.35},{opacity:opacity}],{duration:150,easing:'ease-out'});s.animation=animation;
   animation.onfinish=function(){if(s.animation===animation)s.animation=null;};
  }
  function detach(){cancel(s);component.un('afterrender',render);component.un('show',show);component.un('hide',hide);component.un('destroy',destroy);if(s.elevation&&component.getEl())component.getEl().removeCls('nb-soft-float');var i=states.indexOf(s);if(i>=0)states.splice(i,1);}
  function hide(){cancel(s);}
  function destroy(){detach();}
  s.detach=detach;states.push(s);component.on('afterrender',render);component.on('show',show);component.on('hide',hide);component.on('destroy',destroy);if(component.rendered)render();return detach;
 }
 if(media){if(media.addEventListener)media.addEventListener('change',sync);else if(media.addListener)media.addListener(sync);}
 root.NordicSoftMotion={enable:enable,disable:function(){enable(false);},attach:attach,isEnabled:function(){return enabled;},isReduced:reduced};
})(window);
