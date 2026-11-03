(function(){var D=DFT,M=RATES.mfs,$=D.$;
D.mfsCharge=function(s,amt){return s.flat!=null?s.flat:amt*s.perThousand/1000};
function svcs(){var p=M.providers[$('#prov').value];$('#svc').innerHTML=p.services.map(function(s){return '<option value="'+s.id+'">'+s.name+'</option>'}).join('');}
function run(){var p=M.providers[$('#prov').value],amt=D.num($('#amt').value),out=$('#out');if(!(amt>0)){out.innerHTML='<div class="err">'+D.t('টাকার পরিমাণ লিখুন','Enter an amount')+'</div>';return}
  var s=p.services.filter(function(x){return x.id===$('#svc').value})[0],c=D.mfsCharge(s,amt);
  var h='<div class="result"><div>'+p.name+' — '+s.name+'</div><div class="big" id="total">'+D.t('চার্জ ','Charge ')+D.tk(c)+'</div><div class="kv"><span>'+D.t('একাউন্টে মোট লাগবে','Total needed in account')+'</span><b>'+D.tk(amt+c)+'</b></div>';
  if(s.note)h+='<div class="small muted">'+s.note+'</div>';
  h+='<div class="tbl" style="margin-top:.6rem"><table><tr><th>'+D.t('সেবা','Service')+'</th><th>'+D.t('হার','Rate')+'</th><th>'+D.t('চার্জ','Charge')+'</th></tr>';
  Object.keys(M.providers).forEach(function(k){var P=M.providers[k];P.services.forEach(function(x){h+='<tr><td>'+P.name+' · '+x.name+'</td><td>'+(x.flat!=null?(x.flat?D.tk(x.flat)+D.t(' (ফ্ল্যাট)',' flat'):D.t('ফ্রি','Free')):D.tk(x.perThousand)+D.t('/হাজার','/1000'))+'</td><td>'+D.tk(D.mfsCharge(x,amt))+'</td></tr>'})});
  out.innerHTML=h+'</table></div></div>';}
document.addEventListener('DOMContentLoaded',function(){$('#prov').addEventListener('change',function(){svcs();if($('#out').innerHTML)run()});svcs();$('#calc').addEventListener('click',run);});
document.addEventListener('langchange',function(){if($('#out').innerHTML)run();});
})();
