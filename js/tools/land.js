(function(){var D=DFT,$=D.$;
/* সব একক বর্গফুটে। ১ শতাংশ = ১ ডেসিমেল = ৪৩৫.৬ বর্গফুট (১/১০০ একর); ১ কাঠা = ৭২০ বর্গফুট; ১ ছটাক = ৪৫ বর্গফুট; ১ অযুতাংশ = ১/১০০০০ একর */
var U=[{id:'decimal',bn:'শতাংশ / ডেসিমেল',en:'Decimal (Shotangsho)',sqft:435.6},{id:'katha',bn:'কাঠা',en:'Katha',sqft:720},{id:'bigha',bn:'বিঘা',en:'Bigha',sqft:14374.8},{id:'acre',bn:'একর',en:'Acre',sqft:43560},{id:'sqft',bn:'বর্গফুট',en:'Square feet',sqft:1},{id:'sqm',bn:'বর্গমিটার',en:'Square metre',sqft:10.763910417},{id:'ojutangsho',bn:'অযুতাংশ',en:'Ojutangsho',sqft:4.356},{id:'chhotak',bn:'ছটাক',en:'Chhotak',sqft:45},{id:'hectare',bn:'হেক্টর',en:'Hectare',sqft:107639.10417}];
D.LAND_UNITS=U;
D.setBigha=function(mode){U[2].sqft=mode==='katha20'?14400:33*435.6};
D.landConvert=function(v,from,to){var f=U.filter(function(u){return u.id===from})[0],t=U.filter(function(u){return u.id===to})[0];return v*f.sqft/t.sqft};
function opts(){var sel=$('#from'),cur=sel.value||'bigha';sel.innerHTML=U.map(function(u){return '<option value="'+u.id+'">'+D.t(u.bn,u.en)+'</option>'}).join('');sel.value=cur;}
function run(){D.setBigha($('#bighaMode').value);var v=D.num($('#val').value),f=$('#from').value,out=$('#out');if(!(v>=0)){out.innerHTML='<div class="err">'+D.t('সংখ্যা লিখুন','Enter a number')+'</div>';return}
  var h='<div class="result"><div class="tbl"><table id="convTbl"><tr><th>'+D.t('একক','Unit')+'</th><th>'+D.t('পরিমাণ','Value')+'</th></tr>';
  U.forEach(function(u){if(u.id===f)return;h+='<tr data-u="'+u.id+'"><td>'+D.t(u.bn,u.en)+'</td><td><b>'+D.fmt(D.landConvert(v,f,u.id),4)+'</b></td></tr>'});out.innerHTML=h+'</table></div></div>';}
document.addEventListener('DOMContentLoaded',function(){opts();['val','from','bighaMode'].forEach(function(id){$('#'+id).addEventListener('input',run)});run();});
document.addEventListener('langchange',function(){opts();run();});
})();
