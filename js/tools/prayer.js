(function(){var D=DFT,$=D.$,A=window.adhan;
function params(){var p=A.CalculationMethod.Karachi();p.madhab=A.Madhab.Hanafi;return p}
D.prayerTimes=function(lat,lon,y,m,d){return new A.PrayerTimes(new A.Coordinates(lat,lon),new Date(y,m-1,d,12),params())};
function tf(dt){return D.digits(new Intl.DateTimeFormat('en-US',{hour:'numeric',minute:'2-digit',hour12:true,timeZone:'Asia/Dhaka'}).format(dt)).replace('AM',D.t('এএম','AM')).replace('PM',D.t('পিএম','PM'))}
D.tf=tf;
function dist(){return DISTRICTS[+$('#dist').value]}
function run(){var ds=$('#date').value.split('-').map(Number),z=dist();if(ds.length<3||!z)return;var pt=D.prayerTimes(z.lat,z.lon,ds[0],ds[1],ds[2]);
  var nx=null,now=new Date();var list=[['fajr',D.t('ফজর','Fajr')],['sunrise',D.t('সূর্যোদয়','Sunrise')],['dhuhr',D.t('যোহর','Dhuhr')],['asr',D.t('আসর (হানাফি)','Asr (Hanafi)')],['maghrib',D.t('মাগরিব','Maghrib')],['isha',D.t('এশা','Isha')]];
  list.forEach(function(k){if(!nx&&k[0]!=='sunrise'&&pt[k[0]]>now)nx=k[0]});
  var h='<div class="result"><div class="kv"><span>🌙 '+D.t('সেহরির শেষ সময়','Sehri ends')+'</span><b id="sehri">'+tf(pt.fajr)+'</b></div><div class="kv"><span>🌇 '+D.t('ইফতার','Iftar')+'</span><b id="iftar">'+tf(pt.maghrib)+'</b></div></div>';
  h+='<div class="tbl" style="margin-top:.8rem"><table id="ptTbl"><tr><th>'+D.t('ওয়াক্ত','Prayer')+'</th><th>'+D.t('শুরু','Begins')+'</th></tr>';
  list.forEach(function(k){h+='<tr data-p="'+k[0]+'"'+(k[0]===nx?' class="prayer-now"':'')+'><td>'+k[1]+(k[0]===nx?' ⏰':'')+'</td><td>'+tf(pt[k[0]])+'</td></tr>'});
  $('#out').innerHTML=h+'</table></div>';month();}
function month(){if(!$('#showMonth').checked){$('#month').innerHTML='';return}var ds=$('#date').value.split('-').map(Number),z=dist(),n=new Date(ds[0],ds[1],0).getDate();
  var h='<div class="tbl"><table><tr><th>'+D.t('তারিখ','Date')+'</th><th>'+D.t('সেহরি শেষ','Sehri')+'</th><th>'+D.t('ফজর','Fajr')+'</th><th>'+D.t('যোহর','Dhuhr')+'</th><th>'+D.t('আসর','Asr')+'</th><th>'+D.t('ইফতার/মাগরিব','Iftar')+'</th><th>'+D.t('এশা','Isha')+'</th></tr>';
  for(var d=1;d<=n;d++){var p=D.prayerTimes(z.lat,z.lon,ds[0],ds[1],d);h+='<tr><td>'+D.digits(d)+'</td><td>'+tf(p.fajr)+'</td><td>'+tf(p.fajr)+'</td><td>'+tf(p.dhuhr)+'</td><td>'+tf(p.asr)+'</td><td>'+tf(p.maghrib)+'</td><td>'+tf(p.isha)+'</td></tr>'}
  $('#month').innerHTML=h+'</table></div>';}
function opts(){var s=$('#dist'),cur=s.value;s.innerHTML=DISTRICTS.map(function(z,i){return {z:z,i:i}}).sort(function(a,b){return a.z.bn.localeCompare(b.z.bn,'bn')}).map(function(o){return '<option value="'+o.i+'">'+D.t(o.z.bn,o.z.en)+' ('+o.z.div+')</option>'}).join('');
  s.value=cur||String(DISTRICTS.findIndex(function(z){return z.en==='Dhaka'}));}
document.addEventListener('DOMContentLoaded',function(){opts();try{var sv=localStorage.getItem('dft_dist');if(sv)$('#dist').value=sv}catch(e){}
  var n=new Date();$('#date').value=n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0');
  $('#dist').addEventListener('change',function(){try{localStorage.setItem('dft_dist',this.value)}catch(e){}run()});$('#date').addEventListener('change',run);$('#showMonth').addEventListener('change',month);run();});
document.addEventListener('langchange',function(){opts();run()});
})();
