(function(){var D=DFT,T=RATES.tax,$=D.$;
D.taxCalc=function(o){var salary=o.salary||0,other=o.other||0;
  var exempt=Math.min(salary*T.salaryExemptFraction,T.salaryExemptMax);
  var taxable=Math.max(0,salary-exempt+other);
  var thr=T.thresholds[o.cat||'general']+(o.kids||0)*T.disabledChildExtra;
  var rest=Math.max(0,taxable-thr),tax=0,rows=[[D.t('প্রথম','First')+' '+D.tk(thr,0),Math.min(taxable,thr),0,0]];
  T.slabs.forEach(function(s){if(rest<=0)return;var amt=s.width==null?rest:Math.min(rest,s.width);var t=amt*s.rate/100;tax+=t;rows.push([(s.width==null?D.t('বাকি','Remaining'):D.t('পরবর্তী','Next')+' '+D.tk(s.width,0)),amt,s.rate,t]);rest-=amt;});
  var rebate=Math.min(taxable*T.rebate.pctOfIncome/100,(o.invest||0)*T.rebate.pctOfInvestment/100,T.rebate.max);
  var net=Math.max(0,tax-rebate),minApplied=false;
  if(taxable>thr){var mt=o.newTp?T.minTaxNew:T.minTax;if(net<mt){net=mt;minApplied=true}}
  return {exempt:exempt,taxable:taxable,thr:thr,gross:tax,rebate:rebate,net:net,rows:rows,minApplied:minApplied};};
function run(){var mult=$('#period').value==='m'?12:1;
  var x=D.taxCalc({salary:(D.num($('#salary').value)||0)*mult,other:(D.num($('#other').value)||0)*mult,invest:D.num($('#invest').value)||0,cat:$('#cat').value,kids:D.num($('#kids').value)||0,newTp:$('#newtp').checked});
  var h='<div class="result"><div>'+D.t('বার্ষিক প্রদেয় আয়কর','Annual tax payable')+'</div><div class="big" id="total">'+D.tk(x.net,0)+'</div><div class="muted small">'+D.t('মাসে প্রায় ','≈ per month ')+D.tk(x.net/12,0)+'</div>';
  [[D.t('বেতনের করমুক্ত অংশ (১/৩ বা ৫ লাখ, যেটা কম)','Salary exemption'),x.exempt],[D.t('করযোগ্য আয়','Taxable income'),x.taxable],[D.t('করমুক্ত সীমা','Tax-free threshold'),x.thr],[D.t('রেয়াতের আগে কর','Tax before rebate'),x.gross],[D.t('বিনিয়োগ রেয়াত','Investment rebate'),x.rebate]].forEach(function(k){h+='<div class="kv"><span>'+k[0]+'</span><b>'+D.tk(k[1],0)+'</b></div>'});
  h+='<div class="tbl" style="margin-top:.6rem"><table><tr><th>'+D.t('ধাপ','Slab')+'</th><th>'+D.t('আয়','Income')+'</th><th>%</th><th>'+D.t('কর','Tax')+'</th></tr>';
  x.rows.forEach(function(r){h+='<tr><td>'+r[0]+'</td><td>'+D.tk(r[1],0)+'</td><td>'+D.fmt(r[2])+'%</td><td>'+D.tk(r[3],0)+'</td></tr>'});h+='</table></div>';
  if(x.minApplied)h+='<div class="note">'+D.t('আয় করমুক্ত সীমার বেশি, তাই ন্যূনতম কর প্রযোজ্য হয়েছে।','Minimum tax applied.')+'</div>';
  $('#out').innerHTML=h+'</div>';}
function slabs(){var h='<tr><td>'+D.t('করমুক্ত সীমা (সাধারণ)','Tax-free (general)')+'</td><td>'+D.tk(T.thresholds.general,0)+'</td><td>০%</td></tr>';T.slabs.forEach(function(s){h+='<tr><td>'+(s.width==null?D.t('বাকি আয়','Rest'):D.t('পরবর্তী','Next'))+'</td><td>'+(s.width==null?'—':D.tk(s.width,0))+'</td><td>'+D.fmt(s.rate)+'%</td></tr>'});$('#slabTbl').innerHTML=h;}
document.addEventListener('DOMContentLoaded',function(){slabs();$('#calc').addEventListener('click',run);});
document.addEventListener('langchange',function(){slabs();if($('#out').innerHTML)run();});
})();
