(function(){var D=DFT,P=PACKAGES,$=D.$,ops={gp:1,robi:1,bl:1,tt:1};
function run(){var minGb=D.num($('#minGb').value)||0,maxP=D.num($('#maxP').value)||1e9,days=$('#days').value,sort=$('#sort').value;
  var list=P.packs.filter(function(p){return ops[p.op]&&(p.gb==null||p.gb>=minGb)&&p.price<=maxP&&(days==='all'||(days==='short'?p.days<=7:p.days>=28))});
  list.sort(function(a,b){if(sort==='price')return a.price-b.price;var x=a.gb?a.price/a.gb:1e9,y=b.gb?b.price/b.gb:1e9;return x-y});
  var h='<div class="tbl"><table id="pkTbl"><tr><th>'+D.t('অপারেটর','Operator')+'</th><th>'+D.t('ডেটা','Data')+'</th><th>'+D.t('দাম','Price')+'</th><th>'+D.t('মেয়াদ','Validity')+'</th><th>৳/GB</th></tr>';
  list.forEach(function(p){var o=P.operators[p.op];h+='<tr><td>'+o.name+(o.verified?'':' <span class="pill warn">'+D.t('যাচাই করুন','verify')+'</span>')+'</td><td>'+(p.gb==null?D.t('আনলিমিটেড','Unlimited'):D.digits(p.gb)+' GB')+(p.note?'<div class="small muted">'+p.note+'</div>':'')+(p.code?'<div class="small muted">'+D.digits(p.code)+'</div>':'')+'</td><td>'+D.tk(p.price,0)+'</td><td>'+D.digits(p.days)+D.t(' দিন',' d')+'</td><td>'+(p.gb?D.tk(p.price/p.gb,1):'—')+'</td></tr>'});
  if(!list.length)h+='<tr><td colspan="5">'+D.t('এই ফিল্টারে কোনো প্যাক নেই','No packs match')+'</td></tr>';
  $('#out').innerHTML=h+'</table></div>';}
function srcs(){$('#srcList').innerHTML=Object.keys(P.operators).map(function(k){var o=P.operators[k];return '<li><a href="'+o.url+'" target="_blank" rel="noopener">'+o.name+'</a> — '+(o.verified?'<span class="pill ok">'+D.t('অপারেটরের সাইট থেকে মিলানো','checked on operator site')+'</span> ':'<span class="pill warn">'+D.t('তৃতীয় পক্ষের তালিকা','third-party list')+'</span> '+(o.via||''))+' · '+o.checked+'</li>'}).join('')}
document.addEventListener('DOMContentLoaded',function(){$('#upd').textContent=P.lastUpdated;srcs();
  D.$$('#opChips .chip').forEach(function(c){c.addEventListener('click',function(){ops[c.dataset.op]=!ops[c.dataset.op];c.classList.toggle('on',!!ops[c.dataset.op]);run()})});
  ['minGb','maxP','days','sort'].forEach(function(id){$('#'+id).addEventListener('input',run)});run();});
document.addEventListener('langchange',function(){srcs();run()});
})();
