(function(){var D=DFT,$=D.$;
var TEXTS=['বাংলাদেশ একটি নদীমাতৃক দেশ। এ দেশের মানুষ অতিথিপরায়ণ ও পরিশ্রমী। সবুজ মাঠ, নীল আকাশ আর পাখির গান আমাদের মন ভরিয়ে দেয়।',
'নিয়মিত অনুশীলন করলে টাইপিংয়ের গতি ধীরে ধীরে বাড়ে। প্রথমে নির্ভুলভাবে লেখার চেষ্টা করুন, তারপর গতি বাড়ান। কিবোর্ডের দিকে না তাকিয়ে লেখার অভ্যাস করুন।',
'সরকারি চাকরির পরীক্ষায় কম্পিউটার দক্ষতা যাচাইয়ের জন্য বাংলা ও ইংরেজি টাইপিং পরীক্ষা নেওয়া হয়। তাই আগে থেকে প্রস্তুতি নেওয়া ভালো।',
'শিক্ষাই জাতির মেরুদণ্ড। একটি শিক্ষিত জাতি দেশকে উন্নতির শিখরে নিয়ে যেতে পারে। তাই প্রত্যেক শিশুর জন্য মানসম্মত শিক্ষা নিশ্চিত করা প্রয়োজন।'];
var src='',start=0,timer=null,limit=60,done=false,idx=0;
D.typingStats=function(src,typed,sec){var correct=0;for(var i=0;i<typed.length;i++)if(typed[i]===src[i])correct++;
  var sw=src.split(/\s+/),tw=typed.trim().split(/\s+/).filter(Boolean),cw=0;tw.forEach(function(w,i){if(w===sw[i])cw++});
  var min=Math.max(sec,1)/60;return {wpm:Math.round(cw/min),cpm:Math.round(correct/min),acc:typed.length?Math.round(correct/typed.length*100):0,words:cw}};
function render(){var t=$('#inp').value,h='';for(var i=0;i<src.length;i++){var c=src[i]===' '?' ':src[i],cls=i<t.length?(t[i]===src[i]?'ok':'bad'):(i===t.length?'cur':'');h+=cls?'<span class="'+cls+'">'+c+'</span>':c}$('#src').innerHTML=h;}
function stats(final){var sec=start?Math.min((Date.now()-start)/1000,limit):0,s=D.typingStats(src,$('#inp').value,sec);
  $('#wpm').textContent=D.digits(s.wpm);$('#acc').textContent=D.digits(s.acc)+'%';$('#left').textContent=D.digits(Math.max(0,Math.ceil(limit-sec)));
  if(final){$('#out').innerHTML='<div class="result"><div>'+D.t('ফলাফল','Result')+'</div><div class="big" id="total">'+D.digits(s.wpm)+' WPM</div><div class="kv"><span>'+D.t('নির্ভুলতা','Accuracy')+'</span><b>'+D.digits(s.acc)+'%</b></div><div class="kv"><span>'+D.t('সঠিক শব্দ','Correct words')+'</span><b>'+D.digits(s.words)+'</b></div><div class="kv"><span>'+D.t('অক্ষর/মিনিট','Chars/min')+'</span><b>'+D.digits(s.cpm)+'</b></div></div>'}}
function finish(){done=true;clearInterval(timer);$('#inp').disabled=true;stats(true)}
function reset(next){if(next)idx=(idx+1)%TEXTS.length;src=TEXTS[idx];limit=D.num($('#dur').value)||60;start=0;done=false;clearInterval(timer);var i=$('#inp');i.value='';i.disabled=false;$('#out').innerHTML='';render();stats();}
document.addEventListener('DOMContentLoaded',function(){reset();
  $('#inp').addEventListener('input',function(){if(done)return;if(!start){start=Date.now();timer=setInterval(function(){stats();if((Date.now()-start)/1000>=limit)finish()},250)}render();stats();if(this.value.length>=src.length)finish()});
  $('#restart').addEventListener('click',function(){reset()});$('#next').addEventListener('click',function(){reset(true)});$('#dur').addEventListener('change',function(){reset()});});
})();
