/* ================================================================
   Google AdSense কনফিগ (Auto ads চালু)
   - Publisher ID: ca-pub-6277863204170835 — AdSense স্ক্রিপ্ট ট্যাগটি প্রতিটি পাতার <head>-এ
     src/build.py থেকে বসানো হয় (ID বদলালে build.py-র ADS ভ্যারিয়েবলও বদলান)।
   - ম্যানুয়াল বিজ্ঞাপন চাইলে AdSense-এ "Display ad unit" বানিয়ে তার data-ad-slot নাম্বার
     SLOTS-এ বসান (top / middle / bottom)। ফাঁকা থাকলে স্লটগুলো লুকানো থাকে, শুধু Auto ads চলে।
   - ads.txt থাকে dfaster.com-এর রুটে (repo mdrbnbd/mdrbnbd.github.io)।
   ================================================================ */
window.ADS_CONFIG = {
  ADSENSE_CLIENT: 'ca-pub-6277863204170835',
  SLOTS: { top: '', middle: '', bottom: '' }
};
