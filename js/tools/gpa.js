(function(){var D=DFT,$=D.$;
var G=[['A+',5,80],['A',4,70],['A-',3.5,60],['B',3,50],['C',2,40],['D',1,33],['F',0,0]];
D.markToGrade=function(m){for(var i=0;i<G.length;i++)if(m>=G[i][2])return G[i];return G[6]};
/* GPA = (মূল বিষয়ের পয়েন্টের যোগফল + max(0, ৪র্থ বিষয়ের পয়েন্ট − ২)) ÷ মূল বিষয়ের সংখ্যা, সর্বোচ্চ ৫.০০; কোনো মূল বিষয়ে F হলে ফেল */
D.gpaCalc=function(main,fourth){if(!main.length)return null;var fail=main.some(function(p){return p===0});var sum=main.reduce(function(a,b){return a+b},0);
  var bonus=fourth==null?0:Math.max(0,fourth-2);var raw=(sum+bonus)/main.length;
  return {fail:fail,gpa:fail?0:Math.min(5,raw),without:fail?0:sum/main.length,bonus:bonus};};
var PRE={ssc:['বাংলা','ইংরেজি','গণিত','ধর্ম ও নৈতিক শিক্ষা','তথ্য ও যোগাযোগ প্রযুক্তি','বিজ্ঞান / বাংলাদেশ ও বিশ্বপরিচয়','বিভাগের বিষয় ১','বিভাগের বিষয় ২','বিভাগের বিষয় ৩'],hsc:['বাংলা','ইংরেজি','তথ্য ও যোগাযোগ প্রযুক্তি','বিভাগের বিষয় ১','বিভাগের বিষয় ২','বিভাগের বিষয় ৩']};
function opts(sel){return G.map(function(g){return '<option value="'+g[1]+'"'+(g[0]===sel?' selected':'')+'>'+g[0]+' ('+D.digits(g[1].toFixed(2))+')</option>'}).join('')}
function row(name,grade,fourth){var d=document.createElement('div');d.className='gp-row';d.style.cssText='display:grid;grid-template-columns:1fr 92px 70px 34px;gap:.4rem;margin:.35rem 0;align-items:center';
  d.innerHTML='<input class="nm" value="'+name+'" aria-label="বিষয়"><select class="gr" aria-label="গ্রেড">'+opts(grade||'A+')+'</select><input class="mk" inputmode="numeric" placeholder="নম্বর" aria-label="নম্বর"><button class="btn ghost sm rm" aria-label="মুছুন">✕</button>';
  if(fourth)d.dataset.fourth='1';d.querySelector('.mk').addEventListener('input',function(){var m=D.num(this.value);if(m>=0&&m<=100){d.querySelector('.gr').value=D.markToGrade(m)[1];run()}});
  d.querySelector('.gr').addEventListener('change',run);d.querySelector('.rm').addEventListener('click',function(){d.remove();run()});return d;}
function load(){var e=$('#exam').value,m=$('#mainRows');m.innerHTML='';PRE[e].forEach(function(n){m.appendChild(row(n))});var f=$('#fourthRow');f.innerHTML='';f.appendChild(row('৪র্থ বিষয় (ঐচ্ছিক)','A+',1));run();}
function run(){var main=D.$$('#mainRows .gr').map(function(s){return +s.value});var fs=$('#fourthRow .gr'),use=$('#useFourth').checked;var x=D.gpaCalc(main,use&&fs?+fs.value:null);if(!x){$('#out').innerHTML='';return}
  var h='<div class="result"><div>GPA</div><div class="big" id="total">'+(x.fail?D.t('ফেল (F)','Fail (F)'):D.digits(x.gpa.toFixed(2)))+'</div>';
  if(!x.fail)h+='<div class="kv"><span>'+D.t('৪র্থ বিষয় ছাড়া GPA','GPA without 4th subject')+'</span><b>'+D.digits(x.without.toFixed(2))+'</b></div><div class="kv"><span>'+D.t('৪র্থ বিষয় থেকে যোগ হওয়া পয়েন্ট','Bonus points from 4th')+'</span><b>'+D.digits(x.bonus.toFixed(2))+'</b></div>';
  else h+='<p style="margin:.4rem 0 0">'+D.t('কোনো আবশ্যিক/মূল বিষয়ে F থাকলে পুরো ফলাফল ফেল ধরা হয়।','An F in any main subject means overall fail.')+'</p>';
  $('#out').innerHTML=h+'<div class="small muted">'+D.t('মূল বিষয়: ','Main subjects: ')+D.digits(main.length)+'</div></div>';}
document.addEventListener('DOMContentLoaded',function(){$('#exam').addEventListener('change',load);$('#useFourth').addEventListener('change',run);$('#add').addEventListener('click',function(){$('#mainRows').appendChild(row('নতুন বিষয়'));run()});load();});
document.addEventListener('langchange',run);
})();
