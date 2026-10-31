/* PG AI Solutions — site.js: hero route animation + contact form */
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- hero: code types, stops appear, the shortest route draws blue → pink ---- */
  var s=document.querySelector('.hero');
  if(s){
    var cv=s.querySelector('canvas'),code=s.querySelector('pre'),kmEl=s.querySelector('[data-km]'),gainEl=s.querySelector('[data-gain]');
    var ctx=cv.getContext('2d');
    var LINES=['<span class="k">const</span> stops = <span class="k">await</span> load(<span class="s">"patra.json"</span>)',
      '<span class="k">let</span> route = nearest(stops)','',
      '<span class="k">for</span> (<span class="k">let</span> i = 0; i &lt; 4000; i++) {','  route = twoOpt(route)',
      '  <span class="k">if</span> (!route.improved) <span class="k">break</span>','}','',
      'render(route, {','  from: <span class="s">"#0593C6"</span>,','  to:   <span class="s">"#D83995"</span>','})','',
      '<span class="c">// ready · shipped · kept improving</span>'];
    var W=0,H=0,dpr=1,pts=[],t0=0,raf=0,vis=true,km=0,gain=0;
    var rng=function(x){return function(){x=(x*16807)%2147483647;return x/2147483647;};};
    var d=function(a,b){return Math.hypot(a.x-b.x,a.y-b.y);};
    var build=function(){
      var narrow=W<820,r=rng(23),p=[],n=narrow?9:14,b=narrow?[.05,.5,.95,.78]:[.52,.14,.9,.7],i,k;
      for(i=0;i<n;i++)p.push({x:(b[0]+r()*(b[2]-b[0]))*W,y:(b[1]+r()*(b[3]-b[1]))*H});
      var raw=0;for(i=1;i<p.length;i++)raw+=d(p[i-1],p[i]);
      var left=p.slice(1),o=[p[0]];
      while(left.length){var c=o[o.length-1],bi=0,bd=1e9;left.forEach(function(q,j){var x=d(q,c);if(x<bd){bd=x;bi=j;}});o.push(left.splice(bi,1)[0]);}
      var imp=true;while(imp){imp=false;for(i=0;i<o.length-2;i++)for(k=i+2;k<o.length-1;k++){
        if(d(o[i],o[k])+d(o[i+1],o[k+1])<d(o[i],o[i+1])+d(o[k],o[k+1])-1e-6){var sg=o.slice(i+1,k+1).reverse();o.splice.apply(o,[i+1,sg.length].concat(sg));imp=true;}}}
      var L=0;for(i=1;i<o.length;i++)L+=d(o[i-1],o[i]);km=L/W*14;gain=Math.round((1-L/raw)*100);pts=o;
    };
    var size=function(){var r=s.getBoundingClientRect();dpr=Math.min(2,devicePixelRatio||1);W=r.width;H=r.height;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);build();};
    var ink=function(){return getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()||'#0B1A26';};
    var frame=function(now){
      if(!t0)t0=now;var t=reduce?1e9:now-t0,i;
      ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
      var lines=Math.min(LINES.length,Math.floor(t/230)),html=LINES.slice(0,lines).join('\n')+(lines<LINES.length?' <span class="caret"></span>':'');
      if(code._h!==html){code.innerHTML=html;code._h=html;}
      var R=Math.max(2.5,W*.0026),col=ink();
      for(i=0;i<pts.length;i++){var p=pts[i];if(t<500+i*160)continue;
        ctx.fillStyle=i%3===0?'rgba(216,57,149,.14)':'rgba(5,147,198,.14)';ctx.fillRect(p.x-R*3,p.y-R*3,R*6,R*6);
        ctx.fillStyle=col;ctx.fillRect(p.x-R/2-.5,p.y-R/2-.5,R+1,R+1);}
      var pr=Math.min(1,Math.max(0,(t-1300)/2600)),e=1-Math.pow(1-pr,3);
      if(e>0){var tot=0,sg=[];for(i=1;i<pts.length;i++){sg.push(d(pts[i-1],pts[i]));tot+=sg[i-1];}
        var left=tot*e,g=ctx.createLinearGradient(pts[0].x,pts[0].y,pts[pts.length-1].x,pts[pts.length-1].y),end=pts[0];
        g.addColorStop(0,'#0593C6');g.addColorStop(1,'#D83995');
        ctx.strokeStyle=g;ctx.lineWidth=Math.max(1.4,W*.0013);ctx.lineJoin='miter';ctx.lineCap='square';
        ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);
        for(i=1;i<pts.length&&left>0;i++){var f=Math.min(1,left/sg[i-1]);end={x:pts[i-1].x+(pts[i].x-pts[i-1].x)*f,y:pts[i-1].y+(pts[i].y-pts[i-1].y)*f};ctx.lineTo(end.x,end.y);left-=sg[i-1];}
        ctx.stroke();
        ctx.fillStyle='#0593C6';ctx.fillRect(pts[0].x-R*1.4,pts[0].y-R*1.4,R*2.8,R*2.8);
        if(e>=1){var z=pts[pts.length-1];ctx.fillStyle='#D83995';ctx.fillRect(z.x-R*1.4,z.y-R*1.4,R*2.8,R*2.8);}
        if(kmEl)kmEl.textContent=(km*e).toFixed(1);
        if(gainEl)gainEl.textContent=e>=1?'−'+gain+'%':'…';}
      if(vis&&!(reduce&&e>=1)&&t<9000)raf=requestAnimationFrame(frame);
    };
    size();
    addEventListener('resize',function(){size();t0=performance.now()-1e9;cancelAnimationFrame(raf);raf=requestAnimationFrame(frame);});
    if('IntersectionObserver' in window)new IntersectionObserver(function(en){vis=en[0].isIntersecting;cancelAnimationFrame(raf);if(vis)raf=requestAnimationFrame(frame);}).observe(s);
    raf=requestAnimationFrame(frame);
  }

  /* ---- contact form: AJAX with plain-POST fallback ---- */
  var f=document.querySelector('form.cf');
  if(f&&window.fetch&&window.FormData){
    var T=JSON.parse(f.getAttribute('data-t')),btn=f.querySelector('button'),lbl=btn.querySelector('span'),note=f.querySelector('.note');
    f.querySelectorAll('.who input').forEach(function(r){r.addEventListener('change',function(){f.querySelector('[name=_subject]').value=r.getAttribute('data-subj');});});
    f.addEventListener('submit',function(e){
      e.preventDefault();if(btn.disabled)return;
      var fd=new FormData(f);if(fd.get('_honey'))return;
      btn.disabled=true;lbl.textContent=T.sending;note.className='note';note.textContent='';
      fetch(f.action.replace('formsubmit.co/','formsubmit.co/ajax/'),{method:'POST',headers:{Accept:'application/json'},body:fd})
        .then(function(r){if(!r.ok)throw 0;return r.json();})
        .then(function(){lbl.textContent=T.sent;note.className='note ok';note.textContent=T.thanks;f.reset();setTimeout(function(){btn.disabled=false;lbl.textContent=T.send;},4000);})
        .catch(function(){btn.disabled=false;lbl.textContent=T.send;note.className='note err';note.textContent=T.fail;});
    });
  }
})();
