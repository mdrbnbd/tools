/* ================================================================
   মোবাইল ইন্টারনেট প্যাকেজ — এডিটযোগ্য ডেটা
   verified:true  = অপারেটরের নিজের ওয়েবসাইট থেকে মিলিয়ে নেওয়া (checked তারিখে)
   verified:false = তৃতীয় পক্ষের তালিকা থেকে নেওয়া, অপারেটরের অ্যাপে মিলিয়ে নিন
   নতুন প্যাক যোগ করতে একই ফরম্যাটে একটা লাইন যোগ করুন। কোনো অফার বানিয়ে লিখবেন না।
   ================================================================ */
window.PACKAGES = {
  lastUpdated: '৩ নভেম্বর ২০২৬',
  operators: {
    gp:  { name: 'গ্রামীণফোন', url: 'https://www.grameenphone.com/personal/plans-offers/internet-packages', checked: '৩ নভেম্বর ২০২৬', verified: true },
    robi:{ name: 'রবি', url: 'https://www.robi.com.bd/', checked: '৩ নভেম্বর ২০২৬', verified: false, via: 'priceyoo.com (তৃতীয় পক্ষ)' },
    bl:  { name: 'বাংলালিংক', url: 'https://www.banglalink.net/', checked: '৩ নভেম্বর ২০২৬', verified: false, via: 'bdix.app (তৃতীয় পক্ষ)' },
    tt:  { name: 'টেলিটক', url: 'https://teletalk.com.bd/internet-offers', checked: '৩ নভেম্বর ২০২৬', verified: true }
  },
  // gb: null = আনলিমিটেড (স্পিড সীমিত)
  packs: [
    { op: 'gp', gb: 3,   price: 98,  days: 3,  note: 'বোনাসসহ' },
    { op: 'gp', gb: 7,   price: 118, days: 3,  note: 'বোনাসসহ' },
    { op: 'gp', gb: 15,  price: 198, days: 7,  note: 'বোনাসসহ' },
    { op: 'gp', gb: 30,  price: 219, days: 7,  note: 'বোনাসসহ' },
    { op: 'gp', gb: 20,  price: 499, days: 30, note: 'বোনাসসহ' },
    { op: 'gp', gb: 40,  price: 599, days: 30, note: 'বোনাসসহ' },
    { op: 'gp', gb: 60,  price: 698, days: 30, note: 'বোনাসসহ' },
    { op: 'gp', gb: 100, price: 798, days: 30, note: 'বোনাসসহ' },
    { op: 'gp', gb: null,price: 899, days: 30, note: 'আনলিমিটেড, সর্বোচ্চ ১৫ Mbps' },

    { op: 'robi', gb: 10, price: 299, days: 30 },
    { op: 'robi', gb: 20, price: 399, days: 30 },
    { op: 'robi', gb: 30, price: 499, days: 30 },
    { op: 'robi', gb: 50, price: 699, days: 30 },
    { op: 'robi', gb: 100,price: 999, days: 30 },

    { op: 'bl', gb: 15, price: 299, days: 30 },
    { op: 'bl', gb: 30, price: 449, days: 30 },
    { op: 'bl', gb: 50, price: 590, days: 30 },

    { op: 'tt', gb: 10,  price: 102, days: 7,  code: '*111*97#' },
    { op: 'tt', gb: 5,   price: 191, days: 30, code: '*111*532#' },
    { op: 'tt', gb: 10,  price: 226, days: 30, code: '*111*550#' },
    { op: 'tt', gb: 15,  price: 259, days: 30, code: '*111*777#' },
    { op: 'tt', gb: 30,  price: 359, days: 30, code: '*111*344#' },
    { op: 'tt', gb: 45,  price: 419, days: 30, code: '*111*445#' }
  ]
};
