(function(){var D=DFT,$=D.$;
function norm(s){return s.normalize('NFC').replace(/\u09AF\u09BC/g,'\u09DF').replace(/\u09A1\u09BC/g,'\u09DC').replace(/\u09A2\u09BC/g,'\u09DD')}
D.toBijoy=function(s){return BijoyConv.toBijoy(norm(s))};D.toUni=function(s){return BijoyConv.toUnicode(s)};
function copy(id,btn){var t=$('#'+id);t.select();(navigator.clipboard?navigator.clipboard.writeText(t.value):Promise.reject()).catch(function(){document.execCommand('copy')});var o=btn.textContent;btn.textContent='✓';setTimeout(function(){btn.textContent=o},1200)}
document.addEventListener('DOMContentLoaded',function(){
  $('#b2u').addEventListener('click',function(){$('#uni').value=D.toUni($('#bij').value)});
  $('#u2b').addEventListener('click',function(){$('#bij').value=D.toBijoy($('#uni').value)});
  $('#cpU').addEventListener('click',function(){copy('uni',this)});$('#cpB').addEventListener('click',function(){copy('bij',this)});
  $('#clr').addEventListener('click',function(){$('#uni').value='';$('#bij').value=''});});
})();
