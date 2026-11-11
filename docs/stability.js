'use strict';
const names=['both low','fraction only high','absolute only high','both high'];
function reachable(f,d,a,b){
 const u=Math.log(1/f),v=Math.log(1/d),lower=-a,upper=Math.min(a,Math.log(100/f));
 if(a===0&&b===0)return [(f>=1?1:0)+(d>=1?2:0)];
 const states=[];
 for(let state=0;state<4;state++){
  const fh=!!(state&1),dh=!!(state&2),lo=fh?Math.max(lower,u):lower,hi=fh?upper:Math.min(upper,u),closed=fh||upper<u;
  if(lo>hi||(lo===hi&&!closed))continue;
  if(dh?(closed?hi+b>=v:hi+b>v):lo-b<v)states.push(state);
 }
 return states;
}
function show(){
 const [f,d,a,b]=['f','d','a','b'].map(id=>Number(document.getElementById(id).value));
 const result=document.getElementById('result');
 if(![f,d,a,b].every(Number.isFinite)||f<=0||f>100||d<=0||a<0||b<0||a>2||b>2||['f','d','a','b'].some(id=>document.getElementById(id).value==='')){
  result.textContent='Enter valid positive ratios and bounds from 0 to 2 (fraction ratio at most 100).';result.className='error';document.getElementById('states').textContent='';document.getElementById('independent').textContent='';return;
 }
 const states=reachable(f,d,a,b);result.className='';result.textContent=states.length===1?'Stable under these bounds':'Classification can change under these bounds';
 document.getElementById('states').textContent='Coupled model: '+states.map(i=>names[i]).join('; ')+'.';
 const fs=[],ds=[];if(f*Math.exp(-a)<1)fs.push(0);if(Math.min(100,f*Math.exp(a))>=1)fs.push(1);if(d*Math.exp(-a-b)<1)ds.push(0);if(d*Math.exp(a+b)>=1)ds.push(2);
 const independent=fs.flatMap(x=>ds.map(y=>x+y));
 document.getElementById('independent').textContent='Independent envelope: '+independent.map(i=>names[i]).join('; ')+'. Extra attainable states: '+independent.filter(i=>!states.includes(i)).length+'.';
}
['f','d','a','b'].forEach(id=>document.getElementById(id).addEventListener('input',show));show();
