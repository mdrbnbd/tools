(function(){var D=DFT,$=D.$,img=null,fname='photo';
var P={photo:{w:300,h:300,kb:100,fit:'cover'},sign:{w:300,h:80,kb:60,fit:'contain'},custom:null};
function applyPreset(){var p=P[$('#preset').value];$('#custom').hidden=!!p;if(p){$('#w').value=p.w;$('#h').value=p.h;$('#kb').value=p.kb;$('#fit').value=p.fit}}
function draw(w,h){var c=document.createElement('canvas');c.width=w;c.height=h;var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,w,h);x.imageSmoothingQuality='high';
  var iw=img.naturalWidth,ih=img.naturalHeight,fit=$('#fit').value,off=(D.num($('#offY').value)||0)/100;
  if(fit==='cover'){var s=Math.max(w/iw,h/ih),dw=iw*s,dh=ih*s;x.drawImage(img,(w-dw)/2,(h-dh)/2+(dh-h)/2*off*-1,dw,dh)}
  else if(fit==='contain'){var s2=Math.min(w/iw,h/ih),dw2=iw*s2,dh2=ih*s2;x.drawImage(img,(w-dw2)/2,(h-dh2)/2,dw2,dh2)}
  else x.drawImage(img,0,0,w,h);return c;}
function toBlob(c,q){return new Promise(function(r){c.toBlob(r,'image/jpeg',q)})}
D.compressTo=async function(c,maxKB){var lo=0.05,hi=0.95,best=null,b=await toBlob(c,hi);if(b.size<=maxKB*1024)return {blob:b,q:hi};
  for(var i=0;i<9;i++){var m=(lo+hi)/2;b=await toBlob(c,m);if(b.size<=maxKB*1024){best={blob:b,q:m};lo=m}else hi=m}
  if(!best){b=await toBlob(c,0.05);best={blob:b,q:0.05,over:b.size>maxKB*1024}}return best;};
async function run(){var out=$('#out');if(!img){out.innerHTML='<div class="err">'+D.t('আগে একটি ছবি বেছে নিন','Choose an image first')+'</div>';return}
  var w=Math.round(D.num($('#w').value)),h=Math.round(D.num($('#h').value)),kb=D.num($('#kb').value);if(!(w>0&&h>0&&kb>0&&w<=5000&&h<=5000)){out.innerHTML='<div class="err">'+D.t('সঠিক মাপ দিন','Enter valid size')+'</div>';return}
  var c=draw(w,h),r=await D.compressTo(c,kb),url=URL.createObjectURL(r.blob);
  c.className='preview';out.innerHTML='<div class="result"><div class="big" id="total">'+D.digits(w)+'×'+D.digits(h)+' · '+D.fmt(r.blob.size/1024,1)+' KB</div>'+(r.over?'<div class="err">'+D.t('সর্বনিম্ন মানেও সাইজ সীমার বেশি — মাপ ছোট করুন।','Still over the limit — reduce the size.')+'</div>':'<div class="small muted">'+D.t('JPEG মান ','JPEG quality ')+D.digits(Math.round(r.q*100))+'%</div>')+'<div id="pv" style="margin:.6rem 0"></div><a class="btn" id="dl" download="'+fname+'-'+w+'x'+h+'.jpg" href="'+url+'">⬇ '+D.t('ডাউনলোড','Download')+'</a></div>';
  $('#pv').appendChild(c);D.lastResult={w:w,h:h,size:r.blob.size};}
document.addEventListener('DOMContentLoaded',function(){$('#preset').addEventListener('change',applyPreset);applyPreset();
  $('#file').addEventListener('change',function(e){var f=e.target.files[0];if(!f)return;fname=f.name.replace(/\.[^.]+$/,'').replace(/[^\w-]+/g,'_')||'photo';var u=URL.createObjectURL(f);img=new Image();img.onload=function(){$('#orig').textContent=D.t('মূল ছবি: ','Original: ')+D.digits(img.naturalWidth)+'×'+D.digits(img.naturalHeight)+' · '+D.fmt(f.size/1024,1)+' KB';run()};img.src=u;});
  $('#calc').addEventListener('click',run);['fit','offY'].forEach(function(id){$('#'+id).addEventListener('change',run)});});
D.loadImageURL=function(u){return new Promise(function(r){img=new Image();img.onload=function(){r()};img.src=u})};
})();
