/* dFaster Tools — common helpers (no dependencies) */
(function(){
  var BN='০১২৩৪৫৬৭৮৯';
  var D=window.DFT={};
  D.lang=function(){return document.documentElement.lang==='en'?'en':'bn'};
  D.digits=function(s){s=String(s);return D.lang()==='en'?s:s.replace(/[0-9]/g,function(d){return BN[d]})};
  D.toEn=function(s){return String(s==null?'':s).replace(/[০-৯]/g,function(d){return BN.indexOf(d)})};
  D.num=function(v){if(typeof v==='number')return v;var s=D.toEn(v).replace(/[,\s৳]/g,'');if(s==='')return NaN;return Number(s)};
  D.fmt=function(n,dec){if(!isFinite(n))return '—';dec=dec==null?2:dec;var s=new Intl.NumberFormat('en-IN',{maximumFractionDigits:dec,minimumFractionDigits:0}).format(n);return D.digits(s)};
  D.tk=function(n,dec){return '৳'+D.fmt(n,dec==null?2:dec)};
  D.$=function(s,r){return (r||document).querySelector(s)};D.$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  D.t=function(bn,en){return D.lang()==='en'&&en?en:bn};

  // ---- language toggle (Bangla default) ----
  function applyLang(l){
    document.documentElement.lang=l;
    D.$$('[data-en]').forEach(function(el){if(el.dataset.bn==null)el.dataset.bn=el.innerHTML;el.innerHTML=l==='en'?el.dataset.en:el.dataset.bn});
    D.$$('[data-en-ph]').forEach(function(el){if(el.dataset.bnPh==null)el.dataset.bnPh=el.placeholder;el.placeholder=l==='en'?el.dataset.enPh:el.dataset.bnPh});
    var b=D.$('#langBtn');if(b)b.textContent=l==='en'?'বাংলা':'EN';
    document.dispatchEvent(new CustomEvent('langchange'));
  }
  D.setLang=function(l){try{localStorage.setItem('dft_lang',l)}catch(e){}applyLang(l)};
  document.addEventListener('DOMContentLoaded',function(){
    var l='bn';try{l=localStorage.getItem('dft_lang')||'bn'}catch(e){}
    if(l==='en')applyLang('en');
    var b=D.$('#langBtn');if(b)b.addEventListener('click',function(){D.setLang(D.lang()==='en'?'bn':'en')});
    D.$$('[data-year]').forEach(function(e){e.textContent=D.digits(new Date().getFullYear())});
    initAds();
  });

  // ---- AdSense: renders NOTHING while ADSENSE_CLIENT is empty ----
  function initAds(){
    var c=(window.ADS_CONFIG||{}),id=(c.ADSENSE_CLIENT||'').trim();
    if(!/^ca-pub-\d{10,20}$/.test(id))return; // empty or invalid → no script, no slot
    if(!document.querySelector('script[src*="adsbygoogle.js"]')){ // pages already include the tag in <head>
      var s=document.createElement('script');s.async=true;s.crossOrigin='anonymous';
      s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+id;document.head.appendChild(s);}
    D.$$('.ad-slot').forEach(function(el){
      var slot=(c.SLOTS||{})[el.dataset.slot]||'';if(!slot)return; // Auto ads only when no slot id
      el.classList.add('on');
      el.innerHTML='<div class="small muted">বিজ্ঞাপন</div><ins class="adsbygoogle" style="display:block" data-ad-client="'+id+'" data-ad-slot="'+slot+'" data-ad-format="auto" data-full-width-responsive="true"></ins>';
      (window.adsbygoogle=window.adsbygoogle||[]).push({});
    });
  }

  // ---- PWA ----
  if('serviceWorker' in navigator && location.protocol!=='file:'){
    window.addEventListener('load',function(){var sw=document.querySelector('meta[name=dft-root]');navigator.serviceWorker.register((sw?sw.content:'')+'sw.js').catch(function(){})});
  }
})();
