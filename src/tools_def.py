# -*- coding: utf-8 -*-
CATS = [
 ('calc','হিসাব ও ক্যালকুলেটর','Calculators','🧮'),
 ('text','ছবি ও লেখা','Image & Text','🖼️'),
 ('mobile','মোবাইল ও ইন্টারনেট','Mobile & Internet','📱'),
 ('study','পড়াশোনা','Education','🎓'),
 ('religion','ধর্মীয়','Religious','🕌'),
 ('tutorial','টিউটোরিয়াল','Tutorials','📘'),
]
SRC_NOTE = lambda txt: f'<div class="note">{txt}</div>'

TOOLS = [
dict(slug='electricity-bill', cat='calc', icon='💡', bn='বিদ্যুৎ বিল ক্যালকুলেটর', en='Electricity Bill Calculator',
 desc='DESCO, DPDC, পল্লী বিদ্যুৎসহ সব কোম্পানির আবাসিক ধাপভিত্তিক রেটে মাসিক বিল হিসাব করুন।',
 den='Monthly residential bill using BERC slab rates.', js=['data/rates.js','js/tools/electricity.js'],
 kw='বিদ্যুৎ বিল, DESCO বিল, পল্লী বিদ্যুৎ বিল, ইউনিট রেট',
 body='''
<div class="panel"><div class="row c2">
<div><label for="units" data-en="Units used this month">এই মাসে ব্যবহৃত ইউনিট (kWh)</label><input id="units" inputmode="decimal" placeholder="যেমন ১৫০" data-en-ph="e.g. 150"></div>
<div><label for="company" data-en="Distribution company">বিতরণ কোম্পানি</label><select id="company"><option>DESCO</option><option>DPDC</option><option>পল্লী বিদ্যুৎ (BREB)</option><option>NESCO</option><option>WZPDCL (ওজোপাডিকো)</option><option>BPDB</option></select><div class="small muted" data-en="All companies use the same BERC residential tariff.">সব কোম্পানির আবাসিক রেট একই (BERC নির্ধারিত)।</div></div>
<div><label for="load" data-en="Sanctioned load (kW)">অনুমোদিত লোড (কিলোওয়াট)</label><input id="load" inputmode="decimal"></div>
<div><label for="rent" data-en="Meter rent (Tk, if any)">মিটার ভাড়া (টাকা, যদি থাকে)</label><input id="rent" inputmode="decimal"></div>
</div><div class="btns"><button class="btn" id="calc" data-en="Calculate">হিসাব করুন</button></div><div id="out"></div></div>
<div class="panel"><h2 data-en="Current residential rates">বর্তমান আবাসিক রেট (প্রতি ইউনিট)</h2><div class="tbl"><table id="rateTbl"></table></div>
<div class="note">উৎস: <span id="rsrc"></span>। কার্যকর: <span id="reff"></span>। সর্বশেষ মিলানো: <span id="rchk"></span>। ডিমান্ড চার্জ ধরা হয়েছে প্রতি কিলোওয়াটে মাসে ৳<span id="rdem"></span> ও ভ্যাট <span id="rvat"></span>% — আপনার বিলের কাগজের সাথে মিলিয়ে নিন। প্রিপেইড মিটারে রিবেট বা কোম্পানিভেদে ছোট পার্থক্য থাকতে পারে, তাই এটি আনুমানিক হিসাব।</div></div>
<script>document.addEventListener('DOMContentLoaded',function(){var R=RATES.electricity,D=DFT;D.$('#rsrc').innerHTML='<a href="'+R.newsUrl+'" target="_blank" rel="noopener">'+R.source+'</a>';D.$('#reff').textContent=R.effective;D.$('#rchk').textContent=R.checked;D.$('#rdem').textContent=D.digits(R.demandChargePerKW);D.$('#rvat').textContent=D.digits(R.vatPct)})</script>'''),

dict(slug='income-tax', cat='calc', icon='🧾', bn='বেতন ও আয়কর ক্যালকুলেটর', en='Salary & Income Tax Calculator',
 desc='২০২৬-২৭ করবর্ষের স্ল্যাব অনুযায়ী বেতনের আয়কর, বিনিয়োগ রেয়াত ও মাসিক কর হিসাব।',
 den='Bangladesh personal income tax for FY 2026-27.', js=['data/rates.js','js/tools/tax.js'],
 kw='আয়কর ক্যালকুলেটর, ট্যাক্স স্ল্যাব ২০২৬-২৭, বেতনের কর',
 body='''
<div class="panel"><div class="row c2">
<div><label for="cat" data-en="Taxpayer category">করদাতার ধরন</label><select id="cat"><option value="general">সাধারণ (পুরুষ)</option><option value="woman_senior">নারী / ৬৫ বছর বা তার বেশি</option><option value="disabled_third">প্রতিবন্ধী / তৃতীয় লিঙ্গ</option><option value="freedom_fighter">গেজেটভুক্ত যুদ্ধাহত মুক্তিযোদ্ধা / জুলাই যোদ্ধা</option></select></div>
<div><label for="period" data-en="Amounts are">টাকার হিসাব</label><select id="period"><option value="m">মাসিক</option><option value="y">বার্ষিক</option></select></div>
<div><label for="salary" data-en="Gross salary (incl. bonus)">মোট বেতন (বোনাসসহ)</label><input id="salary" inputmode="decimal" placeholder="যেমন ১,০০,০০০" data-en-ph="e.g. 100000"></div>
<div><label for="other" data-en="Other taxable income">অন্যান্য করযোগ্য আয় (ভাড়া, ব্যবসা ইত্যাদি)</label><input id="other" inputmode="decimal" placeholder="০"></div>
<div><label for="invest" data-en="Eligible investment (yearly)">রেয়াতযোগ্য বিনিয়োগ (বার্ষিক — DPS, সঞ্চয়পত্র, বীমা ইত্যাদি)</label><input id="invest" inputmode="decimal" placeholder="০"></div>
<div><label for="kids" data-en="Disabled children (parents)">প্রতিবন্ধী সন্তানের সংখ্যা (পিতা-মাতার জন্য)</label><input id="kids" inputmode="numeric" placeholder="০"></div>
</div><label style="margin-top:.6rem;font-weight:400"><input type="checkbox" id="newtp"> <span data-en="New taxpayer (min tax ৳1,000)">নতুন করদাতা (ন্যূনতম কর ৳১,০০০)</span></label>
<div class="btns"><button class="btn" id="calc" data-en="Calculate">হিসাব করুন</button></div><div id="out"></div></div>
<div class="panel"><h2 data-en="Tax slabs">করের ধাপ</h2><div class="tbl"><table id="slabTbl"></table></div>
<div class="note">করবর্ষ: <span id="tyr"></span>। উৎস: <span id="tsrc"></span>। সর্বশেষ মিলানো: <span id="tchk"></span>। করমুক্ত সীমা — সাধারণ ৳৪ লাখ, নারী ও ৬৫+ ৳৪.৫ লাখ, প্রতিবন্ধী ও তৃতীয় লিঙ্গ ৳৫.২৫ লাখ, গেজেটভুক্ত মুক্তিযোদ্ধা ৳৫.৫ লাখ। বেতনের ১/৩ বা ৳৫ লাখ (যেটা কম) করমুক্ত। রেয়াত = করযোগ্য আয়ের ৩%, বিনিয়োগের ১০% বা ৳৭.৫ লাখ — যেটা সবচেয়ে কম। এটি সাধারণ ধারণার জন্য; রিটার্ন জমার আগে NBR বা কর আইনজীবীর পরামর্শ নিন।</div></div>
<script>document.addEventListener('DOMContentLoaded',function(){var T=RATES.tax,D=DFT;D.$('#tyr').textContent=T.year;D.$('#tsrc').innerHTML='<a href="'+T.sourceUrl+'" target="_blank" rel="noopener">'+T.source+'</a>';D.$('#tchk').textContent=T.checked})</script>'''),

dict(slug='zakat', cat='calc', icon='🌙', bn='জাকাত ক্যালকুলেটর', en='Zakat Calculator',
 desc='আজকের স্বর্ণ-রুপার দাম ধরে নিসাব ও ২.৫% হারে জাকাতের হিসাব।',
 den='Zakat on cash, gold, silver and business assets.', js=['data/rates.js','js/tools/zakat.js'],
 kw='জাকাত ক্যালকুলেটর, নিসাব, স্বর্ণের দাম ভরি',
 body='''
<div class="panel"><h2 data-en="Prices (per vori)">দাম (প্রতি ভরি)</h2><div class="row c3">
<div><label for="goldP" data-en="Gold 22K per vori">স্বর্ণ ২২ ক্যারেট / ভরি (৳)</label><input id="goldP" inputmode="decimal"></div>
<div><label for="silverP" data-en="Silver 22K per vori">রুপা ২২ ক্যারেট / ভরি (৳)</label><input id="silverP" inputmode="decimal"></div>
<div><label for="basis" data-en="Nisab basis">নিসাব নির্ধারণ</label><select id="basis"><option value="silver">রুপা (সাড়ে ৫২ ভরি) — বেশি সতর্ক মত</option><option value="gold">স্বর্ণ (সাড়ে ৭ ভরি)</option></select></div>
</div><div class="note">ডিফল্ট দাম: <span id="zdate"></span> — <a id="zsrc" target="_blank" rel="noopener"></a>। দাম প্রায়ই বদলায়, তাই আজকের দাম বসিয়ে নিন। ১ ভরি = ১১.৬৬৪ গ্রাম।</div>
<h2 data-en="Your assets">আপনার সম্পদ</h2><div class="row c2">
<div><label for="cash" data-en="Cash & bank balance">নগদ ও ব্যাংক/মোবাইল ব্যাংকিংয়ের টাকা</label><input id="cash" inputmode="decimal" placeholder="০"></div>
<div><label for="goldV" data-en="Gold (vori)">স্বর্ণ (ভরি)</label><input id="goldV" inputmode="decimal" placeholder="০"></div>
<div><label for="silverV" data-en="Silver (vori)">রুপা (ভরি)</label><input id="silverV" inputmode="decimal" placeholder="০"></div>
<div><label for="biz" data-en="Business stock (sale value)">ব্যবসার পণ্য (বিক্রয়মূল্যে)</label><input id="biz" inputmode="decimal" placeholder="০"></div>
<div><label for="recv" data-en="Receivable loans">পাওনা টাকা (যা ফেরত পাওয়ার আশা আছে)</label><input id="recv" inputmode="decimal" placeholder="০"></div>
<div><label for="oth" data-en="Other zakatable assets">অন্যান্য (শেয়ার, সঞ্চয়পত্র ইত্যাদি)</label><input id="oth" inputmode="decimal" placeholder="০"></div>
<div><label for="debt" data-en="Debts due now">পরিশোধযোগ্য ঋণ (বাদ যাবে)</label><input id="debt" inputmode="decimal" placeholder="০"></div>
</div><div class="btns"><button class="btn" id="calc" data-en="Calculate">হিসাব করুন</button></div><div id="out"></div>
<div class="note">এটি সাধারণ হিসাব। ব্যক্তিগত পরিস্থিতিতে (যেমন ব্যবহৃত গয়না, দীর্ঘমেয়াদি ঋণ) মাসআলা ভিন্ন হতে পারে — একজন আলেমের পরামর্শ নিন।</div></div>
<script>document.addEventListener('DOMContentLoaded',function(){var Z=RATES.zakat,D=DFT;D.$('#zdate').textContent=Z.priceDate;var a=D.$('#zsrc');a.href=Z.sourceUrl;a.textContent=Z.source})</script>'''),

dict(slug='age-calculator', cat='calc', icon='🎂', bn='বয়স ক্যালকুলেটর', en='Age Calculator',
 desc='নির্দিষ্ট তারিখে আপনার সঠিক বয়স ও চাকরির বয়সসীমা পার হয়েছে কিনা দেখুন।',
 den='Exact age on a date and job age-limit check.', js=['js/tools/age.js'],
 kw='বয়স ক্যালকুলেটর, চাকরির বয়সসীমা, সরকারি চাকরির বয়স',
 body='''
<div class="panel"><div class="row c2">
<div><label for="dob" data-en="Date of birth">জন্ম তারিখ</label><input type="date" id="dob"></div>
<div><label for="asof" data-en="Calculate age on (e.g. circular date)">যে তারিখে বয়স হিসাব হবে (যেমন বিজ্ঞপ্তির তারিখ)</label><input type="date" id="asof"></div>
<div><label for="maxAge" data-en="Upper age limit (years)">সর্বোচ্চ বয়সসীমা (বছর)</label><input id="maxAge" inputmode="numeric" value="32"></div>
<div><label for="minAge" data-en="Minimum age (years)">ন্যূনতম বয়স (বছর)</label><input id="minAge" inputmode="numeric" value="18"></div>
</div><div class="btns"><span class="small muted" style="align-self:center" data-en="Quick limits:">দ্রুত বয়সসীমা:</span><button class="btn ghost sm" data-age="30">৩০</button><button class="btn ghost sm" data-age="32">৩২</button><button class="btn ghost sm" data-age="35">৩৫</button><button class="btn ghost sm" data-age="37">৩৭</button></div>
<div class="btns"><button class="btn" id="calc" data-en="Calculate">হিসাব করুন</button></div><div id="out"></div>
<div class="note">বয়সসীমা চাকরিভেদে আলাদা (কোটা, বিশেষ শ্রেণির জন্য ছাড় থাকতে পারে)। আবেদনের আগে নিয়োগ বিজ্ঞপ্তিতে বয়স গণনার তারিখ ও নিয়ম দেখে নিন।</div></div>'''),

dict(slug='mfs-charge', cat='calc', icon='💸', bn='বিকাশ/নগদ চার্জ ক্যালকুলেটর', en='bKash / Nagad Charge Calculator',
 desc='ক্যাশ আউট, সেন্ড মানিতে কত টাকা চার্জ কাটবে আর একাউন্টে মোট কত লাগবে জানুন।',
 den='Cash out and send money charges for bKash and Nagad.', js=['data/rates.js','js/tools/mfs.js'],
 kw='বিকাশ ক্যাশ আউট চার্জ, নগদ চার্জ, হাজারে কত টাকা',
 body='''
<div class="panel"><div class="row c3">
<div><label for="prov" data-en="Provider">সেবাদাতা</label><select id="prov"><option value="bkash">বিকাশ</option><option value="nagad">নগদ</option></select></div>
<div><label for="svc" data-en="Service">সেবা</label><select id="svc"></select></div>
<div><label for="amt" data-en="Amount (Tk)">টাকার পরিমাণ</label><input id="amt" inputmode="decimal" placeholder="যেমন ৫,০০০" data-en-ph="e.g. 5000"></div>
</div><div class="btns"><button class="btn" id="calc" data-en="Calculate">হিসাব করুন</button></div><div id="out"></div>
<div class="note" id="mfsNote"></div></div>
<script>document.addEventListener('DOMContentLoaded',function(){var M=RATES.mfs,D=DFT,P=M.providers;D.$('#mfsNote').innerHTML=M.note+' সর্বশেষ মিলানো: '+M.checked+'। উৎস: <a href="'+P.bkash.sourceUrl+'" target="_blank" rel="noopener">বিকাশের ওয়েবসাইট</a>; নগদের হার সংবাদ/তৃতীয় পক্ষের তালিকা থেকে নেওয়া — <a href="'+P.nagad.sourceUrl+'" target="_blank" rel="noopener">নগদ</a> অ্যাপে মিলিয়ে নিন।'})</script>'''),

dict(slug='land-converter', cat='calc', icon='📐', bn='জমির মাপ কনভার্টার', en='Land Measurement Converter',
 desc='শতাংশ, ডেসিমেল, কাঠা, বিঘা, একর, বর্গফুট, বর্গমিটার, অযুতাংশ — এক মাপ থেকে সব মাপে।',
 den='Convert decimal, katha, bigha, acre, sq ft and more.', js=['js/tools/land.js'],
 kw='জমির মাপ, শতাংশ থেকে কাঠা, বিঘা কত শতাংশ, কাঠা কত বর্গফুট',
 body='''
<div class="panel"><div class="row c3">
<div><label for="val" data-en="Value">পরিমাণ</label><input id="val" inputmode="decimal" value="1"></div>
<div><label for="from" data-en="From unit">একক</label><select id="from"></select></div>
<div><label for="bighaMode" data-en="Bigha standard">বিঘার মান</label><select id="bighaMode"><option value="dec33">৩৩ শতাংশ (১৪,৩৭৪.৮ বর্গফুট)</option><option value="katha20">২০ কাঠা (১৪,৪০০ বর্গফুট)</option></select></div>
</div><div id="out"></div></div>
<div class="panel"><h2 data-en="Standard conversions">প্রচলিত হিসাব</h2><ul>
<li>১ শতাংশ = ১ ডেসিমেল = ৪৩৫.৬ বর্গফুট = ১০০ অযুতাংশ</li><li>১ কাঠা = ৭২০ বর্গফুট = ১৬ ছটাক ≈ ১.৬৫ শতাংশ</li><li>১ বিঘা = ৩৩ শতাংশ ≈ ২০ কাঠা</li><li>১ একর = ১০০ শতাংশ = ৪৩,৫৬০ বর্গফুট ≈ ৩ বিঘা ১ শতাংশ</li><li>১ বর্গমিটার = ১০.৭৬৪ বর্গফুট; ১ হেক্টর = ২.৪৭১ একর</li></ul>
<div class="note">এলাকাভেদে (বিশেষ করে বিঘা ও কাঠার) স্থানীয় মাপ আলাদা হতে পারে। দলিল বা খতিয়ানের মাপের সাথে মিলিয়ে নিন।</div></div>'''),

dict(slug='photo-resizer', cat='text', icon='🖼️', bn='ছবি ও সাইন রিসাইজার', en='Photo & Signature Resizer',
 desc='চাকরি ও ভর্তির আবেদনের জন্য ছবি ৩০০×৩০০ (১০০KB) ও স্বাক্ষর ৩০০×৮০ (৬০KB) — ফোনেই, আপলোড ছাড়া।',
 den='Resize photo & signature for BD job/admission forms, in-browser.', js=['js/tools/photo.js'],
 kw='ছবি রিসাইজ ৩০০x৩০০, সিগনেচার ৩০০x৮০, টেলিটক আবেদন ছবি',
 body='''
<div class="panel"><div class="note" style="margin-top:0">🔒 আপনার ছবি কোথাও আপলোড হয় না — সব কাজ আপনার ফোন/কম্পিউটারের ব্রাউজারেই হয়।</div>
<div class="row c2"><div><label for="file" data-en="Choose image">ছবি বেছে নিন</label><input type="file" id="file" accept="image/*"><div class="small muted" id="orig"></div></div>
<div><label for="preset" data-en="Preset">প্রিসেট</label><select id="preset"><option value="photo">ছবি — ৩০০×৩০০ পিক্সেল, সর্বোচ্চ ১০০ KB</option><option value="sign">স্বাক্ষর — ৩০০×৮০ পিক্সেল, সর্বোচ্চ ৬০ KB</option><option value="custom">কাস্টম মাপ</option></select></div></div>
<div class="row c3" id="custom" hidden style="margin-top:.6rem">
<div><label for="w" data-en="Width (px)">প্রস্থ (পিক্সেল)</label><input id="w" inputmode="numeric"></div>
<div><label for="h" data-en="Height (px)">উচ্চতা (পিক্সেল)</label><input id="h" inputmode="numeric"></div>
<div><label for="kb" data-en="Max size (KB)">সর্বোচ্চ সাইজ (KB)</label><input id="kb" inputmode="numeric"></div></div>
<div class="row c2" style="margin-top:.6rem"><div><label for="fit" data-en="Fit">কীভাবে বসবে</label><select id="fit"><option value="cover">কেটে পুরো ঘর ভরাট (ছবির জন্য ভালো)</option><option value="contain">পুরোটা দেখাবে, পাশে সাদা (স্বাক্ষরের জন্য ভালো)</option><option value="stretch">টেনে মাপে আনা</option></select></div>
<div><label for="offY" data-en="Move up/down (crop)">ছবি উপরে/নিচে সরান (কাটার সময়)</label><input type="range" id="offY" min="-100" max="100" value="0" style="width:100%"></div></div>
<div class="btns"><button class="btn" id="calc" data-en="Resize">রিসাইজ করুন</button></div><div id="out"></div></div>'''),

dict(slug='bijoy-unicode', cat='text', icon='🔤', bn='বাংলা ফন্ট কনভার্টার (বিজয় ↔ ইউনিকোড)', en='Bijoy ↔ Unicode Converter',
 desc='SutonnyMJ/বিজয়ে লেখা টেক্সট ইউনিকোডে, আর ইউনিকোড টেক্সট বিজয়ে রূপান্তর করুন।',
 den='Convert Bangla text between Bijoy (SutonnyMJ) and Unicode.', js=['js/vendor/bijoy.js','js/tools/bijoy.js'],
 kw='বিজয় থেকে ইউনিকোড, ইউনিকোড টু বিজয়, SutonnyMJ converter',
 body='''
<div class="panel"><label for="bij" data-en="Bijoy text (ASCII, e.g. SutonnyMJ)">বিজয় টেক্সট (SutonnyMJ ইত্যাদি)</label><textarea id="bij" placeholder="Avwg evsjvq Mvb MvB"></textarea>
<div class="btns"><button class="btn" id="b2u">⬇ বিজয় → ইউনিকোড</button><button class="btn ghost" id="u2b">⬆ ইউনিকোড → বিজয়</button><button class="btn ghost sm" id="cpB" data-en="Copy Bijoy">বিজয় কপি</button></div>
<label for="uni" style="margin-top:.8rem" data-en="Unicode text">ইউনিকোড টেক্সট</label><textarea id="uni" placeholder="আমি বাংলায় গান গাই"></textarea>
<div class="btns"><button class="btn ghost sm" id="cpU" data-en="Copy Unicode">ইউনিকোড কপি</button><button class="btn ghost sm" id="clr" data-en="Clear">মুছুন</button></div>
<div class="note">বিজয় টেক্সট Word-এ SutonnyMJ ফন্টে দেখতে হবে; ইউনিকোড টেক্সট ফেসবুক, ওয়েব ও মোবাইলে সরাসরি পড়া যায়। রূপান্তর ইঞ্জিন: ওপেন সোর্স unicode2ascii (MIT)। খুব বিরল যুক্তাক্ষরে ছোট ভুল হলে হাতে ঠিক করে নিন।</div></div>'''),

dict(slug='bangla-typing-test', cat='text', icon='⌨️', bn='বাংলা টাইপিং টেস্ট', en='Bangla Typing Test',
 desc='বাংলা টাইপিংয়ের গতি (WPM) ও নির্ভুলতা মাপুন — চাকরির পরীক্ষার প্রস্তুতি।',
 den='Measure your Bangla typing speed and accuracy.', js=['js/tools/typing.js'],
 kw='বাংলা টাইপিং টেস্ট, টাইপিং স্পিড, WPM',
 body='''
<div class="panel"><div class="row c3"><div><label for="dur" data-en="Duration">সময়</label><select id="dur"><option value="60">১ মিনিট</option><option value="120">২ মিনিট</option><option value="180">৩ মিনিট</option></select></div>
<div><label data-en="Speed">গতি</label><div class="big" style="font-size:1.4rem;font-weight:700"><span id="wpm">০</span> WPM</div></div>
<div><label data-en="Accuracy / time left">নির্ভুলতা / বাকি সময়</label><div style="font-size:1.2rem;font-weight:700"><span id="acc">০%</span> · <span id="left">৬০</span>s</div></div></div>
<p class="small muted" data-en="Type the text below. The timer starts with your first key.">নিচের লেখাটি হুবহু টাইপ করুন। প্রথম অক্ষর লিখলেই সময় শুরু হবে।</p>
<div class="typing-src" id="src"></div><textarea id="inp" style="margin-top:.6rem" placeholder="এখানে টাইপ করুন…" data-en-ph="Type here…" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"></textarea>
<div class="btns"><button class="btn ghost" id="restart" data-en="Restart">আবার শুরু</button><button class="btn ghost" id="next" data-en="Next text">পরের লেখা</button></div><div id="out"></div>
<div class="note">WPM = প্রতি মিনিটে সঠিক শব্দ। বাংলা লিখতে ফোনে Gboard/Ridmik এবং কম্পিউটারে Avro বা Bijoy কিবোর্ড ব্যবহার করুন।</div></div>'''),

dict(slug='mobile-packages', cat='mobile', icon='📶', bn='মোবাইল প্যাকেজ তুলনা', en='Mobile Package Compare',
 desc='জিপি, রবি, বাংলালিংক, টেলিটকের ইন্টারনেট প্যাক পাশাপাশি — প্রতি GB কত টাকা দেখে সস্তাটা বেছে নিন।',
 den='Compare GP, Robi, Banglalink and Teletalk data packs by price per GB.', js=['data/packages.js','js/tools/packages.js'],
 kw='ইন্টারনেট প্যাকেজ তুলনা, জিপি প্যাক, রবি প্যাক, টেলিটক ইন্টারনেট অফার',
 body='''
<div class="note" style="margin-top:0">⚠️ ডেটা সর্বশেষ হালনাগাদ: <b id="upd"></b>। অফার প্রায়ই বদলায় এবং সিমভেদে আলাদা হয় — কেনার আগে অপারেটরের অ্যাপ বা ডায়াল কোডে মিলিয়ে নিন। "যাচাই করুন" চিহ্নিত প্যাক অপারেটরের নিজের সাইট থেকে মিলানো যায়নি।</div>
<div class="panel"><div class="chips" id="opChips"><button class="chip on" data-op="gp">গ্রামীণফোন</button><button class="chip on" data-op="robi">রবি</button><button class="chip on" data-op="bl">বাংলালিংক</button><button class="chip on" data-op="tt">টেলিটক</button></div>
<div class="row c2"><div><label for="minGb" data-en="Minimum GB">কমপক্ষে কত GB</label><input id="minGb" inputmode="decimal" placeholder="০"></div>
<div><label for="maxP" data-en="Max price">সর্বোচ্চ দাম (৳)</label><input id="maxP" inputmode="decimal" placeholder="যেমন ৫০০"></div>
<div><label for="days" data-en="Validity">মেয়াদ</label><select id="days"><option value="all">সব</option><option value="short">৭ দিন বা কম</option><option value="month">৩০ দিন</option></select></div>
<div><label for="sort" data-en="Sort by">সাজান</label><select id="sort"><option value="pergb">প্রতি GB সবচেয়ে সস্তা</option><option value="price">মোট দাম কম</option></select></div></div>
<div id="out" style="margin-top:.8rem"></div></div>
<div class="panel"><h2 data-en="Sources">উৎস</h2><ul id="srcList"></ul><p class="small muted">ডেটা ফাইল: <code>data/packages.js</code> — নতুন প্যাক সেখানে যোগ/বদল করা যায়।</p></div>'''),

dict(slug='gpa-calculator', cat='study', icon='🎓', bn='SSC/HSC GPA ক্যালকুলেটর', en='SSC / HSC GPA Calculator',
 desc='বিষয়ভিত্তিক গ্রেড বা নম্বর দিয়ে ৪র্থ বিষয়ের নিয়মসহ GPA হিসাব করুন।',
 den='GPA with the 4th (optional) subject rule.', js=['js/tools/gpa.js'],
 kw='GPA ক্যালকুলেটর, SSC GPA, HSC GPA, ৪র্থ বিষয়',
 body='''
<div class="panel"><div class="row c2"><div><label for="exam" data-en="Exam">পরীক্ষা</label><select id="exam"><option value="ssc">SSC / দাখিল</option><option value="hsc">HSC / আলিম</option></select></div>
<div style="align-self:end"><label style="font-weight:400"><input type="checkbox" id="useFourth" checked> <span data-en="Include 4th subject">৪র্থ (ঐচ্ছিক) বিষয় যোগ করুন</span></label></div></div>
<p class="small muted" data-en="Pick a grade, or type marks (0-100) to auto-select the grade. Rename or remove subjects as needed.">প্রতিটি বিষয়ের গ্রেড বেছে নিন, অথবা নম্বর (০–১০০) লিখলে গ্রেড নিজে বসবে। বিষয়ের নাম বদলানো ও মুছে ফেলা যায়। দুই পত্রের বিষয় (যেমন বাংলা ১ম+২য়) একটি বিষয় ধরুন।</p>
<h3 data-en="Main subjects">মূল বিষয়</h3><div id="mainRows"></div><button class="btn ghost sm" id="add" data-en="+ Add subject">+ বিষয় যোগ</button>
<h3 style="margin-top:1rem" data-en="4th subject">৪র্থ বিষয়</h3><div id="fourthRow"></div><div id="out"></div></div>
<div class="panel"><h2 data-en="Grading system">গ্রেডিং পদ্ধতি</h2><div class="tbl"><table><tr><th>নম্বর</th><th>গ্রেড</th><th>পয়েন্ট</th></tr><tr><td>৮০–১০০</td><td>A+</td><td>৫.০০</td></tr><tr><td>৭০–৭৯</td><td>A</td><td>৪.০০</td></tr><tr><td>৬০–৬৯</td><td>A-</td><td>৩.৫০</td></tr><tr><td>৫০–৫৯</td><td>B</td><td>৩.০০</td></tr><tr><td>৪০–৪৯</td><td>C</td><td>২.০০</td></tr><tr><td>৩৩–৩৯</td><td>D</td><td>১.০০</td></tr><tr><td>০–৩২</td><td>F</td><td>০.০০</td></tr></table></div>
<div class="note">৪র্থ বিষয়ের নিয়ম: ৪র্থ বিষয়ের পয়েন্ট থেকে ২ বাদ দিয়ে বাকিটা মূল বিষয়ের যোগফলে যোগ হয়, তারপর শুধু মূল বিষয়ের সংখ্যা দিয়ে ভাগ। GPA সর্বোচ্চ ৫.০০। কোনো মূল বিষয়ে F হলে ফেল; ৪র্থ বিষয়ে F হলে ফেল হয় না।</div></div>'''),

dict(slug='prayer-times', cat='religion', icon='🕌', bn='নামাজ ও সেহরি-ইফতারের সময়', en='Prayer, Sehri & Iftar Times',
 desc='৬৪ জেলার নামাজের সময়সূচি, সেহরির শেষ সময় ও ইফতার — অফলাইনেও কাজ করে।',
 den='Prayer times, sehri and iftar for all 64 districts.', js=['js/vendor/adhan.min.js','data/districts.js','js/tools/prayer.js'],
 kw='নামাজের সময়সূচি, সেহরি ইফতারের সময়, জেলাভিত্তিক নামাজের সময়',
 body='''
<div class="panel"><div class="row c2"><div><label for="dist" data-en="District">জেলা</label><select id="dist"></select></div>
<div><label for="date" data-en="Date">তারিখ</label><input type="date" id="date"></div></div>
<div id="out"></div><label style="margin-top:.8rem;font-weight:400"><input type="checkbox" id="showMonth"> <span data-en="Show full month">পুরো মাসের সময়সূচি দেখুন</span></label><div id="month"></div>
<div class="note">হিসাব পদ্ধতি: University of Islamic Sciences, Karachi (ফজর ও এশা ১৮°), আসর হানাফি মাযহাব — বাংলাদেশে প্রচলিত পদ্ধতি। জেলা সদরের অক্ষাংশ-দ্রাঘিমাংশ ধরে হিসাব করা (ওপেন সোর্স adhan-js)। ইসলামিক ফাউন্ডেশনের ক্যালেন্ডারের সাথে ১–৩ মিনিট পার্থক্য হতে পারে; সতর্কতার জন্য সেহরি কয়েক মিনিট আগে শেষ করুন ও ইফতারে স্থানীয় মসজিদের আযান অনুসরণ করুন।</div></div>'''),
]

SITES = [
 ('📞','VIP Number Finder','রবি/এয়ারটেলের খালি সুন্দর নাম্বার খুঁজুন','https://vip.dfaster.com'),
 ('🔁','dFaster Swap','নিরাপদে পুরনো ফোন কেনা-বেচা','https://swap.dfaster.com'),
 ('👕','dFaster Print','নিজের ডিজাইনে টি-শার্ট ও ব্যাগ','https://dfaster.com/dfaster-print/'),
 ('🛍️','dFaster Shop','অনলাইন শপ ডেমো','https://dfaster.com/shop-demo/'),
]
