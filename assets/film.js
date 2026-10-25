/* PG AI Solutions: scroll film (IT drawings scrubbed by scroll) and service sheets that open from their tiles. */
(function(){
  'use strict';
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  function clamp(v,a,b){return v<a?a:v>b?b:v;}
  function ease(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;}
  function out(x){return 1-Math.pow(1-x,3);}
  function seg(a,s,e){return clamp((a-s)/(e-s),0,1);}

  /* ---------------- film ---------------- */
  var film=document.getElementById('film');
  var jump=function(){};
  if(film){(function(){
    var cv=film.querySelector('.film-cv'),ctx=cv.getContext('2d');
    var caps=[].slice.call(film.querySelectorAll('.film-cap')),btns=[].slice.call(film.querySelectorAll('.film-rail button'));
    var fills=btns.map(function(b){return b.querySelector('i');}),hint=film.querySelector('.film-hint');
    var L={};try{L=JSON.parse(film.getAttribute('data-l')||'{}');}catch(e){}
    var N=4,VW=640,VH=520,W=0,H=0,DPR=1,S=1;
    var MONO='ui-monospace,SFMono-Regular,Menlo,Consolas,monospace',DISP="'Gabarito','Manrope',sans-serif",BODY="'Onest','Inter',sans-serif";
    var C={amb:'#ecd28c',amb2:'#f6e6b4',blue:'#7ea6ff',txt:'#e9ecf7',dim:'#8790b0',panel:'#121b3a',panel2:'#19244c',edge:'rgba(255,255,255,.12)'};

    film.classList.add('js');
    if(reduce)film.classList.add('still');

    function size(){
      var r=cv.getBoundingClientRect();DPR=Math.min(2,window.devicePixelRatio||1);W=r.width;H=r.height;
      cv.width=Math.max(1,Math.round(W*DPR));cv.height=Math.max(1,Math.round(H*DPR));
      S=Math.min(W/592,H/488);
    }
    function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();}
    function dot(x,y,r,c,glow){ctx.save();if(glow){ctx.shadowColor=c;ctx.shadowBlur=glow;}ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=c;ctx.fill();ctx.restore();}
    function win(x,y,w,h,title){
      rr(x,y,w,h,18);ctx.fillStyle=C.panel;ctx.fill();ctx.lineWidth=1.5;ctx.strokeStyle=C.edge;ctx.stroke();
      ctx.save();rr(x,y,w,h,18);ctx.clip();ctx.fillStyle=C.panel2;ctx.fillRect(x,y,w,40);ctx.fillStyle=C.edge;ctx.fillRect(x,y+40,w,1);ctx.restore();
      ['#ff6b5e','#ecd28c','#4fd18b'].forEach(function(c,i){dot(x+22+i*18,y+20,5,c);});
      ctx.font='500 14px '+MONO;ctx.fillStyle=C.dim;ctx.textAlign='center';ctx.fillText(title,x+w/2,y+25);ctx.textAlign='left';
    }

    /* blueprint grid that drifts slowly, so the frame never looks frozen */
    function grid(t){
      var g=34*Math.max(.7,S),ox=(t*6)%g,oy=(t*3)%g;
      ctx.lineWidth=1;ctx.strokeStyle='rgba(130,155,255,.07)';ctx.beginPath();
      for(var x=-g+ox;x<W;x+=g){ctx.moveTo(x,0);ctx.lineTo(x,H);}
      for(var y=-g+oy;y<H;y+=g){ctx.moveTo(0,y);ctx.lineTo(W,y);}
      ctx.stroke();
    }

    /* 1. Code */
    var CODE=['const route = plan(stops);','','function plan(stops) {','  let best = greedy(stops);','  for (let i = 0; i < 4000; i++) {','    const next = twoOpt(best);','    if (cost(next) < cost(best))','      best = next;','  }','  return best;','}','// 26.2 km  →  13.6 km'];
    var KW=/^(const|let|function|for|if|return)$/;
    var TOK=CODE.map(function(line){
      if(/^\s*\/\//.test(line))return [[line,C.dim]];
      var o=[],re=/(\s+|[A-Za-z_]\w*|\d+|[^\sA-Za-z_\d]+)/g,m;
      while((m=re.exec(line))){var s=m[0],c=C.txt;
        if(KW.test(s))c=C.amb;else if(/^\d+$/.test(s))c=C.amb2;else if(/^[A-Za-z_]/.test(s)&&line.charAt(re.lastIndex)==='(')c=C.blue;
        o.push([s,c]);}
      return o;});
    var LS=[],TOTAL=0;CODE.forEach(function(l){LS.push(TOTAL);TOTAL+=l.length+1;});
    function sCode(a,t){
      win(40,24,560,472,'optimizer.js');
      var shown=seg(a,0,.86)*TOTAL,cx=100,cy=96;
      ctx.font='500 17px '+MONO;
      for(var i=0;i<CODE.length;i++){
        if(shown<LS[i])break;
        var y=94+i*29,k=Math.floor(shown-LS[i]),x=100;
        ctx.textAlign='right';ctx.fillStyle='rgba(135,144,176,.5)';ctx.fillText(String(i+1),78,y);ctx.textAlign='left';
        for(var j=0;j<TOK[i].length&&k>0;j++){var s=TOK[i][j][0].slice(0,k);ctx.fillStyle=TOK[i][j][1];ctx.fillText(s,x,y);x+=ctx.measureText(s).width;k-=s.length;}
        cx=x;cy=y;
      }
      if(a<1||Math.floor(t*2)%2===0){ctx.fillStyle=C.amb;ctx.fillRect(cx+2,cy-15,9,20);}
      var p=seg(a,.86,1);
      if(p>0){ctx.save();ctx.globalAlpha*=p;var bx=310,by=446-8*(1-out(p));rr(bx,by,272,40,20);ctx.fillStyle='rgba(236,210,140,.16)';ctx.fill();ctx.strokeStyle='rgba(236,210,140,.6)';ctx.stroke();
        ctx.fillStyle=C.amb2;ctx.font='600 14px '+MONO;ctx.fillText('✓ '+(L.done||'4000 iterations · 13.6 km'),bx+18,by+25);ctx.restore();}
    }

    /* 2. Architecture */
    var NODES=[{k:'Browser',x:30,y:64,ic:'win'},{k:'API',x:255,y:64,ic:'api'},{k:'Optimizer',x:480,y:64,ic:'route'},{k:'Database',x:255,y:336,ic:'db'},{k:'Dashboard',x:480,y:336,ic:'bars'}];
    var NW=130,NH=116;
    var EDGES=[[160,122,255,122,1],[385,122,480,122,1],[320,180,320,336,1],[545,180,545,336,0],[385,394,480,394,0]];
    function icon(n,cx,cy){
      ctx.lineWidth=2.5;ctx.strokeStyle=C.amb;ctx.fillStyle=C.amb;
      if(n.ic==='win'){rr(cx-24,cy-17,48,34,6);ctx.stroke();ctx.beginPath();ctx.moveTo(cx-24,cy-7);ctx.lineTo(cx+24,cy-7);ctx.stroke();}
      else if(n.ic==='api'){ctx.font='700 26px '+MONO;ctx.textAlign='center';ctx.fillText('{ }',cx,cy+9);ctx.textAlign='left';}
      else if(n.ic==='route'){ctx.beginPath();ctx.moveTo(cx-22,cy+12);ctx.lineTo(cx-8,cy-8);ctx.lineTo(cx+6,cy+6);ctx.lineTo(cx+22,cy-12);ctx.stroke();[[-22,12],[-8,-8],[6,6],[22,-12]].forEach(function(p){dot(cx+p[0],cy+p[1],3.5,C.amb);});}
      else if(n.ic==='db'){ctx.beginPath();ctx.ellipse(cx,cy-12,20,7,0,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(cx-20,cy-12);ctx.lineTo(cx-20,cy+12);ctx.ellipse(cx,cy+12,20,7,0,Math.PI,0,true);ctx.lineTo(cx+20,cy-12);ctx.stroke();ctx.beginPath();ctx.ellipse(cx,cy,20,7,0,0,Math.PI);ctx.stroke();}
      else{[[-16,10],[-2,20],[12,14]].forEach(function(b){ctx.fillRect(cx+b[0]-4,cy+14-b[1]*1.4,8,b[1]*1.4);});}
    }
    function sArch(a,t){
      EDGES.forEach(function(e,j){
        var p=out(seg(a,.42+j*.07,.6+j*.07));if(p<=0)return;
        var x=e[0]+(e[2]-e[0])*p,y=e[1]+(e[3]-e[1])*p;
        ctx.save();ctx.setLineDash([6,7]);ctx.lineDashOffset=-t*18;ctx.lineWidth=2;ctx.strokeStyle='rgba(126,166,255,.55)';ctx.beginPath();ctx.moveTo(e[0],e[1]);ctx.lineTo(x,y);ctx.stroke();ctx.restore();
        if(p>=1){
          for(var k=0;k<2;k++){
            var q=(t*.55+j*.27+k*.5)%1;if(e[4]&&k===1)q=1-q;
            dot(e[0]+(e[2]-e[0])*q,e[1]+(e[3]-e[1])*q,4.5,C.amb,14);
          }
        }
      });
      NODES.forEach(function(n,i){
        var p=out(seg(a,i*.08,i*.08+.22));if(p<=0)return;
        ctx.save();ctx.globalAlpha*=p;var cx=n.x+NW/2,cy=n.y+NH/2,s=.86+.14*p;
        ctx.translate(cx,cy);ctx.scale(s,s);ctx.translate(-cx,-cy);
        rr(n.x,n.y,NW,NH,18);ctx.fillStyle=C.panel;ctx.fill();ctx.lineWidth=1.5;ctx.strokeStyle=i===1?'rgba(236,210,140,.55)':C.edge;ctx.stroke();
        icon(n,cx,n.y+46);
        ctx.font='600 15px '+BODY;ctx.fillStyle=C.txt;ctx.textAlign='center';ctx.fillText(n.k,cx,n.y+96);ctx.textAlign='left';
        ctx.restore();
      });
      if(a>.3){var r=(t*.6)%1;ctx.save();ctx.globalAlpha*=(1-r)*.5*seg(a,.3,.45);rr(255-r*14,64-r*14,NW+r*28,NH+r*28,18+r*8);ctx.strokeStyle=C.amb;ctx.lineWidth=1.5;ctx.stroke();ctx.restore();}
    }

    /* 3. Dashboard */
    var BARS=[34,48,41,57,52,66,61,72,69,81,77,90],LINE=[22,30,28,41,38,49,47,58,61,66,72,80];
    function fmt(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,',');}
    function sDash(a,t){
      win(40,24,560,472,'dashboard');
      var k=out(seg(a,.05,.45));
      var K=[[L.orders||'Orders',fmt(1284*k)],[L.route||'Avg route',(26.2-12.6*k).toFixed(1)+' km'],[L.ontime||'On time',Math.round(81+16*k)+'%']];
      K.forEach(function(c,i){var x=60+i*178,y=84,p=out(seg(a,i*.06,.2+i*.06));if(p<=0)return;
        ctx.save();ctx.globalAlpha*=p;rr(x,y+10*(1-p),160,84,14);ctx.fillStyle=C.panel2;ctx.fill();
        ctx.font='500 13px '+BODY;ctx.fillStyle=C.dim;ctx.fillText(c[0],x+16,y+30+10*(1-p));
        ctx.font='800 26px '+DISP;ctx.fillStyle=i===1?C.amb:C.txt;ctx.fillText(c[1],x+16,y+64+10*(1-p));ctx.restore();});
      var x0=70,x1=580,y0=448,h=210,bw=(x1-x0)/BARS.length;
      ctx.strokeStyle='rgba(255,255,255,.07)';ctx.lineWidth=1;ctx.beginPath();for(var g=0;g<4;g++){ctx.moveTo(x0,y0-g*h/3);ctx.lineTo(x1,y0-g*h/3);}ctx.stroke();
      BARS.forEach(function(v,i){var p=out(seg(a,.2+i*.03,.42+i*.03));if(p<=0)return;var bh=v/100*h*p;
        rr(x0+i*bw+6,y0-bh,bw-12,bh,5);ctx.fillStyle=i===BARS.length-1?'rgba(236,210,140,.85)':'rgba(126,166,255,.35)';ctx.fill();});
      var lp=seg(a,.5,.95);
      if(lp>0){var n=(LINE.length-1)*lp,last=null;ctx.save();ctx.lineWidth=3;ctx.strokeStyle=C.amb;ctx.lineJoin='round';ctx.beginPath();
        for(var i=0;i<=Math.ceil(n);i++){var f=Math.min(i,n),i0=Math.floor(f),fr=f-i0,v=LINE[i0]+((LINE[Math.min(i0+1,LINE.length-1)]-LINE[i0])*fr);
          var px=x0+bw/2+f*bw,py=y0-v/100*h;if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);last=[px,py];}
        ctx.stroke();ctx.restore();
        if(last){dot(last[0],last[1],5,C.amb2,16);if(lp>=1){var r=(t*.8)%1;ctx.save();ctx.globalAlpha*=(1-r)*.7;ctx.beginPath();ctx.arc(last[0],last[1],5+r*16,0,Math.PI*2);ctx.strokeStyle=C.amb;ctx.lineWidth=2;ctx.stroke();ctx.restore();}}
      }
    }

    /* 4. Optimization: a real 2-opt run, recorded step by step */
    var PTS=(function(){var s=7,r=function(){s=(s*16807)%2147483647;return s/2147483647;},o=[];
      while(o.length<13){var p=[80+r()*480,110+r()*330],ok=o.every(function(q){return Math.hypot(q[0]-p[0],q[1]-p[1])>70;});if(ok)o.push(p);}return o;})();
    function tlen(tr){var d=0;for(var i=0;i<tr.length;i++){var a=PTS[tr[i]],b=PTS[tr[(i+1)%tr.length]];d+=Math.hypot(a[0]-b[0],a[1]-b[1]);}return d;}
    var TOURS=(function(){var tr=[0,7,2,11,4,9,1,12,5,3,10,6,8],out=[tr.slice()],imp=true;
      while(imp){imp=false;
        for(var i=1;i<tr.length-1&&!imp;i++)for(var j=i+1;j<tr.length&&!imp;j++){
          var nt=tr.slice(0,i).concat(tr.slice(i,j+1).reverse(),tr.slice(j+1));
          if(tlen(nt)<tlen(tr)-.5){tr=nt;out.push(tr.slice());imp=true;}}}
      return out;})();
    var L0=tlen(TOURS[0]),LE=tlen(TOURS[TOURS.length-1]);
    function sOpt(a,t){
      rr(40,24,560,472,22);ctx.fillStyle='rgba(18,27,58,.75)';ctx.fill();ctx.strokeStyle=C.edge;ctx.lineWidth=1.5;ctx.stroke();
      ctx.font='500 14px '+MONO;ctx.fillStyle=C.dim;ctx.fillText('route.optimize()',64,58);
      var idx=Math.round(seg(a,.18,.85)*(TOURS.length-1)),tr=TOURS[idx],len=tlen(tr),km=26.2-12.6*(L0-len)/(L0-LE);
      var lp=out(seg(a,.08,.2));
      if(lp>0){ctx.save();ctx.globalAlpha*=lp;ctx.lineWidth=3;ctx.lineJoin='round';ctx.strokeStyle=idx===TOURS.length-1?C.amb:'rgba(236,210,140,.7)';ctx.beginPath();
        tr.forEach(function(k,i){var p=PTS[k];if(i===0)ctx.moveTo(p[0],p[1]);else ctx.lineTo(p[0],p[1]);});ctx.closePath();ctx.stroke();ctx.restore();
        var tot=len,d=(t*90)%tot,acc=0;
        for(var i=0;i<tr.length;i++){var A=PTS[tr[i]],B=PTS[tr[(i+1)%tr.length]],l=Math.hypot(B[0]-A[0],B[1]-A[1]);
          if(acc+l>=d){var f=(d-acc)/l;dot(A[0]+(B[0]-A[0])*f,A[1]+(B[1]-A[1])*f,6,C.amb2,18);break;}acc+=l;}
      }
      PTS.forEach(function(p,i){var q=out(seg(a,i*.006,.06+i*.006));if(q<=0)return;dot(p[0],p[1],(i===0?8:5.5)*q,i===0?C.amb:C.txt);});
      ctx.textAlign='right';ctx.font='800 30px '+DISP;ctx.fillStyle=C.txt;ctx.fillText(km.toFixed(1)+' km',576,64);
      var g=Math.round((1-km/26.2)*100);
      if(g>0){ctx.font='700 13px '+BODY;var gw=ctx.measureText('−'+g+'%').width+20;rr(576-gw,78,gw,24,12);ctx.fillStyle=C.amb;ctx.fill();ctx.fillStyle='#0f1733';ctx.fillText('−'+g+'%',566,95);}
      ctx.font='500 13px '+MONO;ctx.fillStyle=C.dim;ctx.fillText('2-opt · '+(L.step||'step')+' '+idx+'/'+(TOURS.length-1),576,478);ctx.textAlign='left';
    }

    var SCENES=[sCode,sArch,sDash,sOpt];
    var tx=0,ty=0,ptx=0,pty=0;
    function layer(ch,a,t,alpha,sc){
      ctx.save();ctx.globalAlpha=alpha;
      ctx.translate(W/2+tx,H/2+ty);ctx.scale(S*sc,S*sc);ctx.translate(-VW/2,-VH/2);
      SCENES[ch](a,t);ctx.restore();
    }
    var TR=.16;
    function draw(P,t){
      ctx.setTransform(DPR,0,0,DPR,0,0);ctx.clearRect(0,0,W,H);grid(t);
      var f=Math.min(P*N,N-1e-6),ch=Math.floor(f),loc=f-ch;
      var a=ease(clamp((loc-TR*.5)/.62,0,1));
      if(ch>0&&loc<TR){var m=ease(loc/TR);layer(ch-1,1,t,1-m,1+.07*m);layer(ch,a,t,m,.93+.07*m);}
      else layer(ch,a,t,1,1);
      return f;
    }
    var on=-1;
    function ui(f){
      var ch=Math.min(N-1,Math.floor(f));
      if(ch!==on){on=ch;caps.forEach(function(c,i){c.classList.toggle('on',i===ch);});btns.forEach(function(b,i){if(i===ch)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});}
      fills.forEach(function(el,i){el.style.transform='scaleX('+(reduce?(i===ch?1:0):clamp(f-i,0,1))+')';});
      if(hint)hint.classList.toggle('off',f>.06);
    }

    var cur=0,visible=false,running=false,still=0;
    function progress(){var r=film.getBoundingClientRect(),span=r.height-window.innerHeight;return span>0?clamp(-r.top/span,0,1):0;}
    function frame(now){
      running=false;if(!visible)return;
      var target=progress();cur+=(target-cur)*.14;if(Math.abs(target-cur)<1e-4)cur=target;
      tx+=(ptx-tx)*.08;ty+=(pty-ty)*.08;
      ui(draw(cur,now/1000));
      running=true;requestAnimationFrame(frame);
    }
    function paintStill(){ui(draw((still+.98)/N,0));}

    jump=function(i){
      i=clamp(i|0,0,N-1);
      if(reduce){still=i;paintStill();film.scrollIntoView({block:'start'});return;}
      var r=film.getBoundingClientRect(),span=r.height-window.innerHeight,top=window.pageYOffset+r.top+span*(i+.62)/N;
      if(window.pgLenis)window.pgLenis.scrollTo(top,{duration:1.4});else window.scrollTo({top:top,behavior:'smooth'});
    };
    btns.forEach(function(b,i){b.addEventListener('click',function(){jump(i);});});

    if(fine&&!reduce){
      film.addEventListener('pointermove',function(e){var r=cv.getBoundingClientRect();ptx=((e.clientX-r.left)/r.width-.5)*-16;pty=((e.clientY-r.top)/r.height-.5)*-12;},{passive:true});
      film.addEventListener('pointerleave',function(){ptx=pty=0;});
    }

    size();
    if(window.ResizeObserver)new ResizeObserver(function(){size();if(reduce)paintStill();}).observe(cv);
    else window.addEventListener('resize',function(){size();if(reduce)paintStill();});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){if(reduce)paintStill();});

    if(reduce){paintStill();return;}
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(en){visible=en[0].isIntersecting;if(visible&&!running){running=true;requestAnimationFrame(frame);}},{rootMargin:'100px 0px'}).observe(film);
    }else{visible=true;running=true;requestAnimationFrame(frame);}
  })();}

  /* ---------------- live project screens ---------------- */
  (function(){
    var scr=[].slice.call(document.querySelectorAll('.pj-scr'));
    if(!scr.length||reduce)return;
    function measure(el){var img=el.querySelector('img');if(!img)return;var d=img.getBoundingClientRect().height-el.getBoundingClientRect().height;
      if(d>4){el.style.setProperty('--d',(-d)+'px');el.style.setProperty('--t',Math.max(6,d/38).toFixed(1)+'s');el.classList.add('scrolls');}}
    scr.forEach(function(el){var img=el.querySelector('img');if(img.complete)measure(el);else img.addEventListener('load',function(){measure(el);});});
    window.addEventListener('resize',function(){scr.forEach(measure);});
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(en){en.forEach(function(x){x.target.classList.toggle('run',x.isIntersecting);});},{threshold:.2});scr.forEach(function(el){io.observe(el);});}
    else scr.forEach(function(el){el.classList.add('run');});
  })();

  /* ---------------- service sheets ---------------- */
  var sheet=document.getElementById('sheet');
  if(!sheet||typeof sheet.showModal!=='function')return;
  var panel=sheet.querySelector('.sheet-in'),bg=sheet.querySelector('.sheet-bg'),dyn=sheet.querySelector('.sheet-dyn'),cta=sheet.querySelector('.sheet-cta'),seeIt=sheet.querySelector('[data-film]'),live=sheet.querySelector('.sheet-cta .live');
  var from=null,busy=false,ES='cubic-bezier(.32,.72,0,1)';

  function flip(a,b){return 'translate('+(a.left-b.left)+'px,'+(a.top-b.top)+'px) scale('+(a.width/b.width)+','+(a.height/b.height)+')';}
  function fill(tile){
    dyn.innerHTML='';
    var pj=tile.classList.contains('pj'),ic=tile.querySelector('.ic'),dev=tile.querySelector('.pj-dev'),box=dyn;
    dyn.classList.toggle('is-pj',pj);
    if(pj&&dev){dyn.appendChild(dev.cloneNode(true));box=document.createElement('div');box.className='sheet-txt';dyn.appendChild(box);}
    else if(ic)dyn.appendChild(ic.cloneNode(true));
    var hd=document.createElement('div');hd.className='head';hd.textContent=(pj&&tile.getAttribute('data-kind'))||sheet.getAttribute('data-label')||'';box.appendChild(hd);
    var h=tile.querySelector('h3'),p=tile.querySelector('h3+p'),m=tile.querySelector('.sv-more ul');
    var h2=document.createElement('h3');h2.id='sheet-t';h2.textContent=h?h.textContent:'';box.appendChild(h2);
    if(p)box.appendChild(p.cloneNode(true));
    if(m)box.appendChild(m.cloneNode(true));
    if(seeIt){seeIt.hidden=pj;seeIt.setAttribute('data-ch',tile.getAttribute('data-ch')||'0');}
    if(live){var u=pj&&tile.getAttribute('data-live');live.hidden=!u;if(u)live.href=u;}
  }
  function stagger(){
    var els=[].slice.call(dyn.children).concat([cta]);
    els.forEach(function(el,i){el.animate([{opacity:0,transform:'translateY(10px)'},{opacity:1,transform:'none'}],{duration:380,delay:170+i*45,easing:'cubic-bezier(.23,1,.32,1)',fill:'backwards'});});
  }
  function open(tile){
    if(busy||sheet.open)return;
    from=tile;fill(tile);
    sheet.showModal();
    document.documentElement.classList.add('sheet-open');
    if(window.pgLenis)window.pgLenis.stop();
    sheet.scrollTop=0;
    if(reduce)return;
    busy=true;
    var a=tile.getBoundingClientRect(),b=panel.getBoundingClientRect();
    tile.style.visibility='hidden';
    bg.animate([{opacity:0},{opacity:1}],{duration:360,easing:'ease-out'});
    stagger();
    var an=panel.animate([{transform:flip(a,b)},{transform:'none'}],{duration:520,easing:ES});
    an.onfinish=an.oncancel=function(){busy=false;};
  }
  function finish(then){
    var tile=from;from=null;
    sheet.close();
    document.documentElement.classList.remove('sheet-open');
    if(tile){tile.style.visibility='';}
    if(window.pgLenis)window.pgLenis.start();
    busy=false;
    if(then)then();else if(tile){var b=tile.querySelector('.more');if(b)b.focus({preventScroll:true});}
  }
  function close(then){
    if(busy||!sheet.open)return;
    if(reduce||!from){finish(then);return;}
    busy=true;
    var a=from.getBoundingClientRect(),b=panel.getBoundingClientRect();
    var ok=a.bottom>0&&a.top<window.innerHeight;
    dyn.animate([{opacity:1},{opacity:0}],{duration:120,fill:'forwards'});
    cta.animate([{opacity:1},{opacity:0}],{duration:120,fill:'forwards'});
    bg.animate([{opacity:1},{opacity:0}],{duration:300,easing:'ease-out',fill:'forwards'});
    var an=panel.animate(ok?[{transform:'none'},{transform:flip(a,b)}]:[{transform:'none',opacity:1},{transform:'scale(.96)',opacity:0}],{duration:ok?340:220,easing:'cubic-bezier(.4,0,.2,1)',fill:'forwards'});
    an.onfinish=function(){
      finish(then);
      [panel,bg,dyn,cta].forEach(function(el){el.getAnimations().forEach(function(x){x.cancel();});});
    };
  }

  document.addEventListener('click',function(e){
    var t=e.target.closest&&e.target.closest('.s,.pj');
    if(!t||!t.querySelector('.more'))return;
    if(e.target.closest('a'))return;
    open(t);
  });
  sheet.addEventListener('cancel',function(e){e.preventDefault();close();});
  sheet.addEventListener('click',function(e){
    if(e.target===sheet||e.target===bg||(e.target.closest&&e.target.closest('.sheet-x'))){close();return;}
    var go=e.target.closest&&e.target.closest('.sheet-cta a');
    if(!go||go.classList.contains('live'))return;
    e.preventDefault();e.stopPropagation();
    var ch=go.getAttribute('data-film'),href=go.getAttribute('href');
    close(function(){
      if(ch!==null){jump(+go.getAttribute('data-ch'));return;}
      var el=document.querySelector(href);if(!el)return;
      if(window.pgLenis)window.pgLenis.scrollTo(el,{offset:-24});else el.scrollIntoView({behavior:reduce?'auto':'smooth'});
    });
  });
})();
