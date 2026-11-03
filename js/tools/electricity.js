(function(){var D=DFT,R=RATES.electricity,$=D.$;
function calc(units){var rows=[],energy=0;
  if(units<=R.lifeline.max){energy=units*R.lifeline.rate;rows.push([D.t('লাইফলাইন (০–','Lifeline (0–')+D.digits(R.lifeline.max)+')',units,R.lifeline.rate,energy]);}
  else{var prev=0;R.slabs.forEach(function(s){if(units<=prev)return;var top=s.upto==null?units:Math.min(units,s.upto),u=top-prev;if(u>0){rows.push([D.digits(prev+1)+'–'+(s.upto==null?D.t('তার বেশি','above'):D.digits(s.upto)),u,s.rate,u*s.rate]);energy+=u*s.rate;}prev=s.upto==null?units:s.upto;});}
  return {rows:rows,energy:energy};}
D.elecCalc=function(units,load,rent){var c=calc(units);var demand=load*R.demandChargePerKW;var vat=(c.energy+demand)*R.vatPct/100;return {rows:c.rows,energy:c.energy,demand:demand,vat:vat,rent:rent,total:c.energy+demand+vat+rent};};
function run(){var u=D.num($('#units').value),l=D.num($('#load').value)||0,r=D.num($('#rent').value)||0,out=$('#out');
  if(!(u>=0)){out.innerHTML='<div class="err">'+D.t('সঠিক ইউনিট লিখুন','Enter valid units')+'</div>';return;}
  var x=D.elecCalc(u,l,r);
  var h='<div class="result"><div>'+D.t('মোট আনুমানিক বিল','Estimated total bill')+'</div><div class="big" id="total">'+D.tk(x.total)+'</div>';
  h+='<div class="tbl"><table><tr><th>'+D.t('ধাপ','Slab')+'</th><th>'+D.t('ইউনিট','Units')+'</th><th>'+D.t('হার','Rate')+'</th><th>'+D.t('টাকা','Taka')+'</th></tr>';
  x.rows.forEach(function(r){h+='<tr><td>'+r[0]+'</td><td>'+D.fmt(r[1])+'</td><td>'+D.tk(r[2])+'</td><td>'+D.tk(r[3])+'</td></tr>'});
  h+='</table></div>';
  [[D.t('এনার্জি চার্জ','Energy charge'),x.energy],[D.t('ডিমান্ড চার্জ','Demand charge')+' ('+D.fmt(l)+' kW × ৳'+D.fmt(R.demandChargePerKW)+')',x.demand],[D.t('ভ্যাট','VAT')+' '+D.fmt(R.vatPct)+'%',x.vat],[D.t('মিটার ভাড়া','Meter rent'),x.rent]].forEach(function(k){h+='<div class="kv"><span>'+k[0]+'</span><b>'+D.tk(k[1])+'</b></div>'});
  out.innerHTML=h+'</div>';}
function rates(){var h='<tr><td>'+D.t('লাইফলাইন (মাসে মোট ','Lifeline (total ≤ ')+D.digits(R.lifeline.max)+D.t(' ইউনিট পর্যন্ত)',' units)')+'</td><td>'+D.tk(R.lifeline.rate)+'</td></tr>',prev=0;
  R.slabs.forEach(function(s){h+='<tr><td>'+D.digits(prev+(prev?1:0))+'–'+(s.upto==null?D.t('তার বেশি','above'):D.digits(s.upto))+' '+D.t('ইউনিট','units')+'</td><td>'+D.tk(s.rate)+'</td></tr>';prev=s.upto});
  $('#rateTbl').innerHTML=h;}
document.addEventListener('DOMContentLoaded',function(){$('#load').value=R.defaultLoadKW;$('#rent').value=R.defaultMeterRent;rates();$('#calc').addEventListener('click',run);$('#units').addEventListener('keydown',function(e){if(e.key==='Enter')run()});});
document.addEventListener('langchange',function(){rates();if($('#out').innerHTML)run();});
})();
