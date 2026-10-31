/* Hero v4: code types on the left, stops light up and the optimal route draws blue → pink. */
(function(){
  var s=document.querySelector('.r4');if(!s)return;
  var cv=s.querySelector('canvas'),code=s.querySelector('.r4-code'),kmEl=s.querySelector('[data-km]'),gainEl=s.querySelector('[data-gain]');
  var ctx=cv.getContext('2d'),reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var LINES=[
    '<span class="r4k">const</span> stops = <span class="r4k">await</span> load(<span class="r4s">"patra.json"</span>)',
    '<span class="r4k">let</span> route = nearest(stops)','',
    '<span class="r4k">for</span> (<span class="r4k">let</span> i = 0; i &lt; 4000; i++) {',
    '  route = twoOpt(route)',
    '  <span class="r4k">if</span> (!route.improved) <span class="r4k">break</span>','}','',
    'render(route, {',
    '  from: <span class="r4s">"#0593C6"</span>,',
    '  to:   <span class="r4s">"#D83995"</span>','})','',
    '<span class="r4c">// ready · shipped · kept improving</span>'];
  var W=0,H=0,dpr=1,pts=null,t0=0,raf=0,visible=true,km=0,gain=0;
  function rng(x){return function(){x=(x*16807)%2147483647;return x/2147483647;};}
  function d(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
  function build(){
    var narrow=W<700,r=rng(23),p=[],n=narrow?10:14,b=narrow?[.5,.06,.94,.34]:[.36,.1,.64,.78];
    for(var i=0;i<n;i++)p.push({x:(b[0]+r()*(b[2]-b[0]))*W,y:(b[1]+r()*(b[3]-b[1]))*H});
    var raw=0;for(i=1;i<p.length;i++)raw+=d(p[i-1],p[i]);
    var left=p.slice(1),o=[p[0]];
    while(left.length){var c=o[o.length-1],bi=0,bd=1e9;left.forEach(function(q,j){var k=d(q,c);if(k<bd){bd=k;bi=j;}});o.push(left.splice(bi,1)[0]);}
    var imp=true;while(imp){imp=false;for(i=0;i<o.length-2;i++)for(var k=i+2;k<o.length-1;k++){
      if(d(o[i],o[k])+d(o[i+1],o[k+1])<d(o[i],o[i+1])+d(o[k],o[k+1])-1e-6){var seg=o.slice(i+1,k+1).reverse();o.splice.apply(o,[i+1,seg.length].concat(seg));imp=true;}}}
    var L=0;for(i=1;i<o.length;i++)L+=d(o[i-1],o[i]);
    km=L/W*14;gain=Math.round((1-L/raw)*100);pts=o;
  }
  function size(){var r=s.getBoundingClientRect();dpr=Math.min(2,window.devicePixelRatio||1);W=r.width;H=r.height;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);build();}
  function orb(x,y,r,c){var g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,c);g.addColorStop(1,'rgba(5,12,19,0)');ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);}
  function frame(now){
    if(!t0)t0=now;var t=reduce?1e9:now-t0;
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
    var s1=t/5000;orb(W*(.8+.03*Math.sin(s1)),H*.38,W*.45,'rgba(216,57,149,.22)');orb(W*(.55+.03*Math.cos(s1)),H*.95,W*.38,'rgba(5,147,198,.26)');
    var lines=Math.min(LINES.length,Math.floor(t/240)),html=LINES.slice(0,lines).join('\n')+(lines<LINES.length?' <span class="r4-caret"></span>':'');
    if(code._h!==html){code.innerHTML=html;code._h=html;}
    var dotR=Math.max(1.6,W*.0022);
    pts.forEach(function(p,i){if(t<500+i*170)return;var a=.4+.3*Math.sin(t/900+i*1.7),c=i%3===0?'240,107,180':'63,180,224',g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,dotR*9);
      g.addColorStop(0,'rgba('+c+','+(a*.55)+')');g.addColorStop(1,'rgba('+c+',0)');ctx.fillStyle=g;ctx.fillRect(p.x-dotR*9,p.y-dotR*9,dotR*18,dotR*18);
      ctx.beginPath();ctx.arc(p.x,p.y,dotR,0,7);ctx.fillStyle='rgba(234,243,249,'+(.55+a*.45)+')';ctx.fill();});
    var pr=Math.min(1,Math.max(0,(t-1300)/2600)),e=1-Math.pow(1-pr,3);
    if(e>0){var tot=0,segs=[],i;for(i=1;i<pts.length;i++){segs.push(d(pts[i-1],pts[i]));tot+=segs[i-1];}
      var left=tot*e,g2=ctx.createLinearGradient(pts[0].x,pts[0].y,pts[pts.length-1].x,pts[pts.length-1].y),end=pts[0];
      g2.addColorStop(0,'#3FB4E0');g2.addColorStop(1,'#F06BB4');
      ctx.save();ctx.strokeStyle=g2;ctx.lineWidth=Math.max(1,W*.0012);ctx.lineCap=ctx.lineJoin='round';ctx.shadowColor='rgba(216,57,149,.65)';ctx.shadowBlur=10;
      ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);
      for(i=1;i<pts.length&&left>0;i++){var f=Math.min(1,left/segs[i-1]);end={x:pts[i-1].x+(pts[i].x-pts[i-1].x)*f,y:pts[i-1].y+(pts[i].y-pts[i-1].y)*f};ctx.lineTo(end.x,end.y);left-=segs[i-1];}
      ctx.stroke();ctx.restore();
      if(e<1){ctx.beginPath();ctx.arc(end.x,end.y,dotR*1.6,0,7);ctx.fillStyle='#fff';ctx.fill();}
      if(kmEl)kmEl.textContent=(km*e).toFixed(1);
      if(gainEl)gainEl.textContent=e>=1?'−'+gain+'%':'…';}
    if(visible&&!(reduce&&e>=1))raf=requestAnimationFrame(frame);
  }
  size();
  window.addEventListener('resize',function(){size();if(reduce)frame(performance.now());});
  if('IntersectionObserver' in window)new IntersectionObserver(function(en){visible=en[0].isIntersecting;cancelAnimationFrame(raf);if(visible)raf=requestAnimationFrame(frame);}).observe(s);
  raf=requestAnimationFrame(frame);
})();
