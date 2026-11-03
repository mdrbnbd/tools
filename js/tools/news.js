/* News page: Bangla (machine-translated in the GitHub Action) by default in BN mode; originals in EN mode. */
(function(){var D=DFT,$=D.$,data=null,globalOrig=false,itemOrig={};
try{globalOrig=localStorage.getItem('dft_news_orig')==='1'}catch(e){}
function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function when(iso){if(!iso)return '';var d=new Date(iso);if(isNaN(d))return '';var m=Math.round((Date.now()-d)/6e4);
  if(m<60)return D.t(D.digits(Math.max(m,1))+' মিনিট আগে',m+' min ago');if(m<1440)return D.t(D.digits(Math.round(m/60))+' ঘণ্টা আগে',Math.round(m/60)+' h ago');
  return d.toLocaleDateString(D.lang()==='en'?'en-GB':'bn-BD',{timeZone:'Asia/Dhaka',day:'numeric',month:'short'})}
function render(){var box=$('#newsList'),bn=D.lang()!=='en',g=$('#origAll');
  $('#newsCtl').hidden=!bn;g.textContent=globalOrig?'বাংলায় দেখুন':'মূল ইংরেজি দেখুন';g.setAttribute('aria-pressed',globalOrig?'true':'false');
  if(!data){return}var src=$('#newsSrc');
  src.innerHTML=D.t('উৎস: ','Sources: ')+data.sources.map(function(s){return '<a href="'+esc(s.url)+'" rel="noopener" target="_blank">'+esc(s.name)+'</a>'}).join(', ')+' · '+D.t('হালনাগাদ: ','Updated: ')+esc(new Date(data.updated).toLocaleString(bn?'bn-BD':'en-GB',{timeZone:'Asia/Dhaka',dateStyle:'medium',timeStyle:'short'}))+D.t(' (ঢাকা সময়)',' (Dhaka time)');
  if(!data.items.length){box.innerHTML='<p class="muted">'+D.t('এখন কোনো খবর নেই।','No news right now.')+'</p>';return}
  box.innerHTML=data.items.map(function(it,i){var has=!!it.title_bn,orig=!bn||globalOrig||itemOrig[it.link]||!has;
    var t=orig?it.title:it.title_bn,s=orig?it.snippet:(it.snippet_bn||it.snippet);
    var tog=bn&&has?'<button type="button" class="chip sm news-tog" data-i="'+i+'" aria-pressed="'+(orig?'true':'false')+'">'+(orig?'বাংলা':'মূল ইংরেজি')+'</button>':'';
    var mark=bn&&!has?'<span class="pill">ইংরেজি — অনুবাদ নেই</span>':(bn&&!orig?'<span class="pill">স্বয়ংক্রিয় অনুবাদ</span>':'');
    return '<article class="news-item" lang="'+(orig?'en':'bn')+'"><h3><a href="'+esc(it.link)+'" target="_blank" rel="noopener">'+esc(t)+'</a></h3>'+(s?'<p>'+esc(s)+'</p>':'')+
      '<div class="news-meta"><span>'+esc(it.source)+' · '+when(it.published)+'</span>'+mark+tog+'</div></article>'}).join('');
  D.$$('.news-tog',box).forEach(function(b){b.addEventListener('click',function(){var it=data.items[+b.dataset.i],cur=globalOrig||itemOrig[it.link];
    if(globalOrig&&cur){globalOrig=false;try{localStorage.setItem('dft_news_orig','0')}catch(e){}data.items.forEach(function(x){itemOrig[x.link]=true});itemOrig[it.link]=false}else itemOrig[it.link]=!cur;render()})})}
document.addEventListener('DOMContentLoaded',function(){
  $('#origAll').addEventListener('click',function(){globalOrig=!globalOrig;itemOrig={};try{localStorage.setItem('dft_news_orig',globalOrig?'1':'0')}catch(e){}render()});
  fetch((document.querySelector('meta[name=dft-root]').content||'')+'news.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(j){data=j;D.newsData=j;render()})
  .catch(function(){$('#newsList').innerHTML='<div class="err">'+D.t('খবর লোড করা যায়নি। ইন্টারনেট সংযোগ দেখুন।','Could not load news.')+'</div>'});render()});
document.addEventListener('langchange',render);
})();
