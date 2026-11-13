/* PG AI Solutions — site.js: hero solver animation, scroll reveals, contact form */
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- hero: scattered stops → real 2-opt solver → PG monogram → a day's route, then rest (see DESIGN.md · Motion) ---- */
  var s=document.querySelector('.hero');
  if(s){
    var c=s.querySelector('canvas'),x=c.getContext('2d'),hud=s.querySelector('.hud');
    var $=function(k){return hud.querySelector('[data-'+k+']');},nEl=$('n'),itEl=$('it'),kmEl=$('km'),barEl=$('bar');
    var css=function(k,d){return getComputedStyle(document.documentElement).getPropertyValue(k).trim()||d;};
    var fmt=new Intl.NumberFormat(document.documentElement.lang||'en');
    var PATH='M12 54 V10 H30 A11 11 0 0 1 30 32 H12 M48 32 C48 44 54 54 66 54 C75 54 82 47 84 36 H68 M48 32 C48 20 54 10 66 10 C74 10 80 14 83 20';
    var W,H,dpr,mob,N,box,sc,GAP,PG,P,ord=[],mode,state,tS,tM,first,it=0,sweepI,improved,pulse=0,lineA=0,km0=1,stops=0,raf=0,vis=true,seed;
    var r=function(){seed=(seed*9301+49297)%233280;return seed/233280;};
    var eo=function(t){return 1-Math.pow(1-t,4);},eio=function(t){return t<.5?8*t*t*t*t:1-Math.pow(-2*t+2,4)/2;};
    var D=function(a,b){return Math.hypot(P[a].tx-P[b].tx,P[a].ty-P[b].ty);};
    var len=function(){var t=0;for(var i=1;i<ord.length;i++)t+=D(ord[i-1],ord[i]);return t;};
    function layout(){
      var rc=s.getBoundingClientRect();W=rc.width;H=rc.height;dpr=Math.min(2,devicePixelRatio||1);
      c.width=Math.round(W*dpr);c.height=Math.round(H*dpr);x.setTransform(dpr,0,0,dpr,0,0);
      mob=W<820;N=mob?70:110;
      var tx=s.querySelector('.hero-txt').getBoundingClientRect(),bx=Math.max(W*.5,tx.right-rc.left+48);
      box=mob?{x:W*.1,y:H*.04,w:W*.8,h:Math.min(H*.17,W*.6)}:{x:bx,y:H*.07,w:Math.max(W*.3,W*.95-bx),h:H*.42};
      sc=Math.min(box.w/76,box.h/48);
      var ox=box.x+(box.w-76*sc)/2-8*sc,oy=box.y+(box.h-48*sc)/2-8*sc;
      var ns='http://www.w3.org/2000/svg',sv=document.createElementNS(ns,'svg'),pa=document.createElementNS(ns,'path');
      pa.setAttribute('d',PATH);sv.appendChild(pa);sv.style.cssText='position:absolute;width:0;height:0;visibility:hidden';document.body.appendChild(sv);
      var TL=pa.getTotalLength();PG=[];for(var i=0;i<N;i++){var q=pa.getPointAtLength(TL*i/N);PG.push([ox+q.x*sc,oy+q.y*sc]);}
      sv.remove();GAP=TL*sc/N*2.2;
    }
    function randLayout(){var L=[];for(var i=0;i<N;i++)L.push([box.x+r()*box.w,box.y+r()*box.h]);return L;}
    function greedy(){var u={0:1},o=[0];while(o.length<N){var b=-1,bd=1e9;for(var i=0;i<N;i++)if(!u[i]){var d=D(o[o.length-1],i);if(d<bd){bd=d;b=i;}}o.push(b);u[b]=1;}return o;}
    // one improving 2-opt move per call (best move for the current i) → the untangling is visible
    function sweep(){for(var b=0;b<N;b++){if(sweepI>=N-1){if(!improved)return true;improved=false;sweepI=1;}var i=sweepI,best=0,bj=-1;
      for(var j=i+1;j<N;j++){var nx=j<N-1?D(ord[j],ord[j+1]):0,nn=j<N-1?D(ord[i],ord[j+1]):0,g=D(ord[i-1],ord[i])+nx-D(ord[i-1],ord[j])-nn;if(g>best+1e-9){best=g;bj=j;}}
      it++;if(bj>0){var sg=ord.slice(i,bj+1).reverse();Array.prototype.splice.apply(ord,[i,sg.length].concat(sg));improved=true;return false;}sweepI++;}return false;}
    function go(next,now,isFirst){mode=next;first=isFirst;var T=next==='pg'?PG:randLayout();
      P.forEach(function(p,i){p.fx=isFirst?box.x+r()*box.w:p.x;p.fy=isFirst?box.y+r()*box.h:p.y;p.tx=T[i][0];p.ty=T[i][1];p.d=isFirst?200+r()*700:r()*350;});
      state='move';tS=tM=now;}
    function start(now){seed=23;layout();P=PG.map(function(){return {x:0,y:0,a:0};});ord=[];it=0;stops=0;lineA=0;
      if(reduce){P.forEach(function(p,i){p.tx=PG[i][0];p.ty=PG[i][1];});mode='route';var T=randLayout();P.forEach(function(p,i){p.x=p.tx=T[i][0];p.y=p.ty=T[i][1];p.a=1;});
        ord=greedy();sweepI=1;improved=false;while(!sweep());state='rest';lineA=1;km0=len();stops=N;return;}
      go('pg',now,true);}
    function draw(now){
      var t=now-tS,i,hold=state==='hold'||state==='rest';
      if(state==='move'||state==='solve'||(state==='hold'&&mode==='pg'))P.forEach(function(p){var dur=first?1000:1300,k=Math.min(1,Math.max(0,(now-tM-p.d)/dur)),e=first?eo(k):eio(k);p.x=p.fx+(p.tx-p.fx)*e;p.y=p.fy+(p.ty-p.fy)*e;p.a=first?Math.min(1,k*2):1;});
      if(state==='move'){lineA=Math.max(0,lineA-.06);if(t>(first?1500:1750)){ord=greedy();km0=len();sweepI=1;improved=false;state='solve';tS=now;}}
      else if(state==='solve'){lineA=Math.min(1,lineA+.05);if(t>350&&sweep()){state=mode==='pg'?'hold':'rest';tS=now;}}
      else if(state==='hold'&&t>2600)go('route',now,false);
      x.clearRect(0,0,W,H);
      var g=x.createLinearGradient(box.x,0,box.x+box.w,0);g.addColorStop(0,'#0593C6');g.addColorStop(1,'#D83995');
      var hk=hold?Math.min(1,(now-tS)/500):0;if(reduce)hk=1;
      if(ord.length&&lineA>0){x.lineJoin='round';x.lineCap='round';
        var far=function(a,b){return mode==='pg'&&Math.hypot(a.tx-b.tx,a.ty-b.ty)>GAP;};
        if(hold){x.globalAlpha=.22*hk*lineA;x.strokeStyle=g;x.lineWidth=10;x.filter='blur(8px)';x.beginPath();
          for(i=0;i<N;i++){var p=P[ord[i]];if(i&&!far(p,P[ord[i-1]]))x.lineTo(p.x,p.y);else x.moveTo(p.x,p.y);}x.stroke();x.filter='none';}
        x.strokeStyle=g;x.lineWidth=1.4+1.6*hk;
        for(i=1;i<N;i++){var a=P[ord[i-1]],b=P[ord[i]],f=far(a,b);x.globalAlpha=lineA*(f?(hold?.12:.35):(.7+.3*hk));x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke();}
        x.globalAlpha=1;}
      P.forEach(function(p,i){x.globalAlpha=p.a;var dep=mode==='route'&&ord[0]===i&&lineA>.5;x.fillStyle=dep?'#0593C6':css('--dot','#E9EEF8');x.beginPath();x.arc(p.x,p.y,dep?5:(mode==='route'?2.6:1.8),0,7);x.fill();});
      x.globalAlpha=1;
      if(hold&&!reduce){pulse=(pulse+.0024)%1;var ff=pulse*(N-1),k=Math.floor(ff),u=ff-k,A=P[ord[k]],B=P[ord[k+1]],px=A.x+(B.x-A.x)*u,py=A.y+(B.y-A.y)*u;
        var rg=x.createRadialGradient(px,py,0,px,py,22);rg.addColorStop(0,css('--glow','rgba(255,255,255,.85)'));rg.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=rg;x.beginPath();x.arc(px,py,22,0,7);x.fill();}
      var cur=ord.length&&state!=='move'?len():km0*2.4;stops=Math.min(N,stops+2);
      nEl.textContent=stops;itEl.textContent=fmt.format(it);kmEl.textContent=(cur/(14*W/1280)).toFixed(1)+' km';
      barEl.style.transform='scaleX('+(hold?1:state==='solve'?Math.min(.97,.3+.67*Math.max(0,(km0-cur)/(km0*.3))):.15)+')';
    }
    function frame(now){draw(now);if(vis&&!(reduce||(state==='rest'&&document.hidden)))raf=requestAnimationFrame(frame);}
    start(performance.now());
    if(reduce)draw(performance.now());else raf=requestAnimationFrame(frame);
    var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){var w=s.getBoundingClientRect().width;if(Math.abs(w-W)<2)return;cancelAnimationFrame(raf);start(performance.now());if(reduce)draw(performance.now());else raf=requestAnimationFrame(frame);},200);});
    if('IntersectionObserver' in window)new IntersectionObserver(function(en){vis=en[0].isIntersecting;cancelAnimationFrame(raf);if(vis&&!reduce)raf=requestAnimationFrame(frame);}).observe(s);
  }

  /* ---- theme toggle: light / dark, remembered per visitor ---- */
  var tb=document.querySelector('.theme');
  if(tb){var root=document.documentElement,cur=function(){return root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');};
    var sync=function(){tb.setAttribute('aria-pressed',cur()==='light'?'true':'false');};sync();
    tb.addEventListener('click',function(){var n=cur()==='light'?'dark':'light';root.setAttribute('data-theme',n);try{localStorage.setItem('pg-theme',n)}catch(e){}sync();});}

  /* ---- headline: one gradient across the accent phrase, sliced per word ---- */
  var paint=function(){document.querySelectorAll('.h1').forEach(function(h){var g=h.querySelectorAll('.g');if(!g.length)return;
    var L=Infinity,R=-Infinity;g.forEach(function(w){var b=w.getBoundingClientRect();L=Math.min(L,b.left);R=Math.max(R,b.right);});
    g.forEach(function(w){w.style.backgroundSize=(R-L)+'px 100%';w.style.backgroundPosition=(L-w.getBoundingClientRect().left)+'px 0';});});};
  paint();addEventListener('resize',paint);if(document.fonts)document.fonts.ready.then(paint);

  /* ---- scroll reveals: prompt types itself, then chips and plan; cards clip in; counters count up ---- */
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var el=e.target;
    if(el.classList.contains('prompt')){var q=el.getAttribute('data-q'),pin=el.querySelector('.pin'),j=0;
      var done=function(){var ch=el.querySelector('.chips');ch.querySelectorAll('span').forEach(function(sp,i){sp.style.transitionDelay=i*60+'ms';});ch.classList.add('on');
        el.querySelectorAll('.plan div').forEach(function(d,i){setTimeout(function(){d.classList.add('on');},300+i*180);});};
      if(reduce){pin.textContent=q;done();}else(function ty(){pin.textContent=q.slice(0,++j);if(j<q.length)setTimeout(ty,22);else done();})();}
    else el.classList.add('on');});},{rootMargin:'0px 0px -12% 0px'}):null;
  document.querySelectorAll('.prompt,.rv').forEach(function(el,i){if(!io){el.classList.add('on');var pq=el.querySelector&&el.querySelector('.pin');if(pq){pq.textContent=el.getAttribute('data-q');el.querySelectorAll('.chips,.plan div').forEach(function(z){z.classList.add('on');});}return;}
    if(el.classList.contains('rv'))el.style.transitionDelay=(Array.prototype.indexOf.call(el.parentNode.children,el)%4)*70+'ms';io.observe(el);});

  /* ---- contact form: AJAX with plain-POST fallback ---- */
  var f=document.querySelector('form.cf');
  if(f&&window.fetch&&window.FormData){
    var T=JSON.parse(f.getAttribute('data-t')),btn=f.querySelector('button'),lbl=btn.querySelector('span'),note=f.querySelector('.note');
    f.querySelectorAll('.who input').forEach(function(r){r.addEventListener('change',function(){f.querySelector('[name=_subject]').value=r.getAttribute('data-subj');});});
    f.addEventListener('submit',function(e){
      e.preventDefault();if(btn.disabled)return;
      var fd=new FormData(f);if(fd.get('_gotcha'))return;
      btn.disabled=true;lbl.textContent=T.sending;note.className='note';note.textContent='';
      fetch(f.action,{method:'POST',headers:{Accept:'application/json'},body:fd})
        .then(function(r){if(!r.ok)throw 0;return r.json();})
        // Formspree answers {ok:true} when the message was accepted for delivery;
        // anything else (errors, limits) is shown as a failure, never as "sent".
        .then(function(j){if(!j||j.ok!==true)throw 0;lbl.textContent=T.sent;note.className='note ok';note.textContent=T.thanks;f.reset();setTimeout(function(){btn.disabled=false;lbl.textContent=T.send;},4000);})
        .catch(function(){btn.disabled=false;lbl.textContent=T.send;note.className='note err';note.textContent=T.fail;});
    });
  }
})();
