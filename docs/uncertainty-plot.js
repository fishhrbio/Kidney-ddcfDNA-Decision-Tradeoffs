'use strict';
function drawUncertainty(){
 const svg=document.getElementById('uncertainty-plot'),summary=document.getElementById('plot-summary');
 const [f,d,a,b]=['f','d','a','b'].map(id=>Number(document.getElementById(id).value));
 svg.querySelectorAll('.drawing').forEach(el=>el.remove());
 if(![f,d,a,b].every(Number.isFinite)||f<=0||f>100||d<=0||a<0||b<0||a>2||b>2||['f','d','a','b'].some(id=>document.getElementById(id).value==='')){summary.textContent='Enter valid values to draw the uncertainty region.';return;}
 const ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');g.setAttribute('class','drawing');svg.appendChild(g);
 function add(tag,attrs,text){const el=document.createElementNS(ns,tag);for(const [key,value] of Object.entries(attrs))el.setAttribute(key,value);if(text!==undefined)el.textContent=text;g.appendChild(el);return el;}
 const x0=Math.log(f),y0=Math.log(d),up=Math.min(a,Math.log(100/f)),xmin=x0-a,xmax=x0+up,ymin=y0-a-b,ymax=y0+a+b;
 // Show threshold and the entire region, with a common span on log axes.
 const lo=Math.min(-1.6,xmin,ymin)-.25,hi=Math.max(1.6,xmax,ymax)+.25;
 const X=x=>80+(x-lo)/(hi-lo)*520,Y=y=>385-(y-lo)/(hi-lo)*330;
 const zx=X(0),zy=Y(0),width=X(hi)-X(lo),height=Y(lo)-Y(hi);
 add('rect',{x:80,y:55,width,height,fill:'#f7f9f8',stroke:'#d9dfde'});
 add('rect',{x:zx,y:55,width:X(hi)-zx,height:zy-55,fill:'#edf3f4'});
 const ticks=[lo,0,hi];
 for(const t of ticks){add('line',{x1:X(t),y1:55,x2:X(t),y2:385,stroke:'#d9dfde','stroke-dasharray':'3 5'});add('line',{x1:80,y1:Y(t),x2:600,y2:Y(t),stroke:'#d9dfde','stroke-dasharray':'3 5'});const value=Math.exp(t);const label=value<.01||value>100?value.toExponential(1):value.toFixed(2).replace(/\.00$/,'');add('text',{x:X(t),y:407,'text-anchor':'middle','font-size':11,fill:'#50616c'},label);add('text',{x:70,y:Y(t)+4,'text-anchor':'end','font-size':11,fill:'#50616c'},label);}
 add('line',{x1:zx,y1:55,x2:zx,y2:385,stroke:'#50616c','stroke-dasharray':'5 5'});add('line',{x1:80,y1:zy,x2:600,y2:zy,stroke:'#50616c','stroke-dasharray':'5 5'});
 const corners=[[-a,-b],[-a,b],[up,b],[up,-b]].map(([ef,et])=>`${X(x0+ef)},${Y(y0+ef+et)}`).join(' ');
 add('polygon',{id:'coupled-region',points:corners,fill:'#176b8733',stroke:'#176b87','stroke-width':3,'vector-effect':'non-scaling-stroke'});
 if(document.getElementById('compare').checked)add('rect',{id:'independent-region',x:X(xmin),y:Y(ymax),width:X(xmax)-X(xmin),height:Y(ymin)-Y(ymax),fill:'none',stroke:'#b06a21','stroke-width':2,'stroke-dasharray':'7 5','vector-effect':'non-scaling-stroke'});
 add('circle',{cx:X(x0),cy:Y(y0),r:5,fill:'#172f3e',stroke:'white','stroke-width':2});
 add('text',{x:340,y:445,'text-anchor':'middle','font-size':13,fill:'#172f3e'},'Fraction / fraction threshold (log scale)');
 add('text',{x:17,y:225,transform:'rotate(-90 17 225)','text-anchor':'middle','font-size':13,fill:'#172f3e'},'Concentration / concentration threshold (log scale)');
 add('text',{x:80,y:30,'font-size':11,fill:'#50616c'},'Dashed threshold lines at 1 · illustrative design space');
 const states=reachable(f,d,a,b);summary.textContent=`At this baseline, ${states.length} classification state${states.length===1?' is':'s are'} attainable under the coupled bounds. ${a===0&&b===0?'With zero uncertainty, the region is a point.':b===0?'With no total-cfDNA error, the coupled region is a line.':'The blue region preserves shared error.'}`;
 document.getElementById('plot-desc').textContent=summary.textContent+' Threshold equality is assigned to high. This is a hypothetical scenario, not a rejection-risk estimate.';
}
['f','d','a','b','compare'].forEach(id=>document.getElementById(id).addEventListener('input',drawUncertainty));drawUncertainty();
