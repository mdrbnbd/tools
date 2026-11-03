(function(){var D=DFT,$=D.$;
function parse(s){var m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s);return m?{y:+m[1],m:+m[2],d:+m[3]}:null}
function dim(y,m){return new Date(Date.UTC(y,m,0)).getUTCDate()}
D.ageDiff=function(a,b){var k=(b.y-a.y)*12+(b.m-a.m);if(cmp(addMonths(a,k),b)>0)k--;var s=addMonths(a,k),d=Math.round((Date.UTC(b.y,b.m-1,b.d)-Date.UTC(s.y,s.m-1,s.d))/864e5);return {y:Math.floor(k/12),m:k%12,d:d}};
function addMonths(a,n){var t=a.y*12+(a.m-1)+n,y=Math.floor(t/12),m=t%12+1;return {y:y,m:m,d:Math.min(a.d,dim(y,m))}}
function addYears(a,n){var y=a.y+n,d=Math.min(a.d,dim(y,a.m));return {y:y,m:a.m,d:d}}
function cmp(a,b){return (a.y-b.y)||(a.m-b.m)||(a.d-b.d)}
function fd(o){return D.digits(String(o.d).padStart(2,'0')+'/'+String(o.m).padStart(2,'0')+'/'+o.y)}
function run(){var a=parse($('#dob').value),b=parse($('#asof').value),mx=D.num($('#maxAge').value),mn=D.num($('#minAge').value),out=$('#out');
  if(!a||!b||cmp(a,b)>0){out.innerHTML='<div class="err">'+D.t('সঠিক জন্মতারিখ ও হিসাবের তারিখ দিন','Enter valid dates')+'</div>';return}
  var g=D.ageDiff(a,b),h='<div class="result"><div>'+D.t('বয়স','Age')+' ('+fd(b)+D.t(' তারিখে',' as of')+')</div><div class="big" id="total">'+D.digits(g.y)+D.t(' বছর ',' y ')+D.digits(g.m)+D.t(' মাস ',' m ')+D.digits(g.d)+D.t(' দিন',' d')+'</div>';
  if(mx>0){var lim=addYears(a,mx);var ok=cmp(b,lim)<=0;
    h+='<p style="margin:.5rem 0 0"><b>'+(ok?'✅ '+D.t('সর্বোচ্চ বয়সসীমার মধ্যে আছেন','Within the upper age limit'):'❌ '+D.t('সর্বোচ্চ বয়সসীমা পার হয়ে গেছে','Over the upper age limit'))+'</b> ('+D.digits(mx)+D.t(' বছর',' y')+')</p>';
    h+='<p class="small muted" style="margin:.2rem 0 0">'+D.t('আপনার '+D.digits(mx)+' বছর পূর্ণ হয় ','You turn '+mx+' on ')+fd(lim)+D.t(' তারিখে।','.')+'</p>';}
  if(mn>0){var lo=addYears(a,mn);h+='<p style="margin:.3rem 0 0">'+(cmp(b,lo)>=0?'✅ '+D.t('ন্যূনতম বয়স ('+D.digits(mn)+') পূর্ণ','Minimum age met'):'❌ '+D.t('ন্যূনতম বয়স ('+D.digits(mn)+') পূর্ণ হয়নি — পূর্ণ হবে ','Minimum age not met — reached on ')+fd(lo))+'</p>'}
  var tot=Math.round((Date.UTC(b.y,b.m-1,b.d)-Date.UTC(a.y,a.m-1,a.d))/864e5);h+='<p class="small muted" style="margin:.3rem 0 0">'+D.t('মোট ','Total ')+D.fmt(tot,0)+D.t(' দিন',' days')+'</p>';
  out.innerHTML=h+'</div>';}
document.addEventListener('DOMContentLoaded',function(){var n=new Date();$('#asof').value=n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0');
  D.$$('[data-age]').forEach(function(b){b.addEventListener('click',function(){$('#maxAge').value=b.dataset.age;run()})});$('#calc').addEventListener('click',run);});
document.addEventListener('langchange',function(){if($('#out').innerHTML)run();});
})();
