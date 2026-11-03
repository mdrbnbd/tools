(function(){var D=DFT,Z=RATES.zakat,$=D.$;
D.zakatCalc=function(o){var assets=o.cash+o.goldVori*o.goldPrice+o.silverVori*o.silverPrice+o.business+o.receivable+o.other;var net=assets-o.debt;
  var nisab=o.basis==='gold'?Z.nisabGoldVori*o.goldPrice:Z.nisabSilverVori*o.silverPrice;var due=net>=nisab&&net>0;return {assets:assets,net:net,nisab:nisab,due:due,zakat:due?net*Z.rate/100:0};};
function v(id){return D.num($('#'+id).value)||0}
function run(){var x=D.zakatCalc({cash:v('cash'),goldVori:v('goldV'),silverVori:v('silverV'),goldPrice:v('goldP'),silverPrice:v('silverP'),business:v('biz'),receivable:v('recv'),other:v('oth'),debt:v('debt'),basis:$('#basis').value});
  var h='<div class="result"><div>'+D.t('প্রদেয় জাকাত','Zakat payable')+'</div><div class="big" id="total">'+D.tk(x.zakat,0)+'</div>';
  [[D.t('মোট সম্পদ','Total assets'),x.assets],[D.t('ঋণ বাদে নিট সম্পদ','Net assets'),x.net],[D.t('নিসাব','Nisab'),x.nisab]].forEach(function(k){h+='<div class="kv"><span>'+k[0]+'</span><b>'+D.tk(k[1],0)+'</b></div>'});
  h+='<p style="margin:.6rem 0 0">'+(x.due?D.t('আপনার নিট সম্পদ নিসাব পরিমাণের বেশি, তাই ২.৫% জাকাত ফরজ (এক চান্দ্র বছর পূর্ণ হলে)।','Net assets exceed nisab: 2.5% zakat due.'):D.t('নিট সম্পদ নিসাবের কম, জাকাত ফরজ নয়।','Below nisab: no zakat due.'))+'</p></div>';$('#out').innerHTML=h;}
document.addEventListener('DOMContentLoaded',function(){$('#goldP').value=Z.goldPerVori22k;$('#silverP').value=Z.silverPerVori22k;$('#calc').addEventListener('click',run);});
document.addEventListener('langchange',function(){if($('#out').innerHTML)run();});
})();
