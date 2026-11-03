/* ================================================================
   dFaster Tools — সব রেট/হার এক জায়গায় (এডিট করার জন্য)
   হার বদলালে শুধু এই ফাইলের সংখ্যা বদলান, তারপর sw.js-এর VERSION এক বাড়ান।
   ================================================================ */
window.RATES = {

  /* ---------- বিদ্যুৎ বিল (আবাসিক LT-A) ---------- */
  electricity: {
    effective: 'জুন ২০২৬ বিল মাস থেকে',
    checked: '৩ নভেম্বর ২০২৬',
    source: 'BERC আদেশ ৩ জুন ২০২৬ ও পুনর্বিবেচনা আদেশ ২০২৬/০১ (৪ জুন ২০২৬)',
    sourceUrl: 'https://berc.org.bd/',
    newsUrl: 'https://www.thedailystar.net/news/environment/natural-resources/energy/news/berc-withdraws-electricity-price-hike-low-use-residential-consumers-4190646',
    // মাসে মোট ব্যবহার lifeline.max বা তার কম হলে সব ইউনিট lifeline রেটে
    lifeline: { max: 50, rate: 4.63 },
    // ধাপভিত্তিক (telescopic) হার — upto: এই ধাপের শেষ ইউনিট (null = এর উপরে সব)
    slabs: [
      { upto: 75,  rate: 5.26 },
      { upto: 200, rate: 8.50 },
      { upto: 300, rate: 9.10 },
      { upto: 400, rate: 9.62 },
      { upto: 600, rate: 15.01 },
      { upto: null, rate: 17.35 }
    ],
    demandChargePerKW: 42,   // ডিমান্ড চার্জ (টাকা/কিলোওয়াট/মাস) — অফিসের বিলের সাথে মিলিয়ে নিন
    vatPct: 5,               // ভ্যাট (%) — এনার্জি চার্জ + ডিমান্ড চার্জের উপর
    defaultLoadKW: 2,
    defaultMeterRent: 0      // মিটার ভাড়া (পোস্টপেইডে কোম্পানিভেদে থাকে) — ব্যবহারকারী বদলাতে পারবেন
  },

  /* ---------- আয়কর (ব্যক্তি করদাতা) ---------- */
  tax: {
    year: '২০২৬-২৭ করবর্ষ (আয়বর্ষ জুলাই ২০২৬ – জুন ২০২৭)',
    checked: '৩ নভেম্বর ২০২৬',
    source: 'অর্থ আইন ২০২৬ (Finance Bill 2026 পাস, সংশোধিত); PwC Worldwide Tax Summaries (৩১ জুলাই ২০২৬ রিভিউ)',
    sourceUrl: 'https://taxsummaries.pwc.com/bangladesh/individual/taxes-on-personal-income',
    newsUrl: 'https://www.thedailystar.net/business/economy/news/money-whitening-provision-ends-tax-free-income-threshold-raised-4211621',
    thresholds: {           // করমুক্ত আয়সীমা
      general: 400000,
      woman_senior: 450000,   // নারী ও ৬৫+ বছর
      disabled_third: 525000, // প্রতিবন্ধী ও তৃতীয় লিঙ্গ
      freedom_fighter: 550000 // গেজেটভুক্ত যুদ্ধাহত মুক্তিযোদ্ধা / জুলাই যোদ্ধা
    },
    disabledChildExtra: 50000, // প্রতিবন্ধী সন্তানের পিতা-মাতা: প্রতি সন্তানে অতিরিক্ত
    slabs: [ // করমুক্ত সীমার পরের ধাপ
      { width: 300000, rate: 10 },
      { width: 400000, rate: 15 },
      { width: 500000, rate: 20 },
      { width: 2000000, rate: 25 },
      { width: null, rate: 30 }
    ],
    salaryExemptFraction: 1/3, salaryExemptMax: 500000, // বেতন আয়ের ১/৩ বা ৫ লাখ, যেটা কম
    rebate: { pctOfIncome: 3, pctOfInvestment: 10, max: 750000 },
    minTax: 5000, minTaxNew: 1000
  },

  /* ---------- জাকাত ---------- */
  zakat: {
    priceDate: '২ নভেম্বর ২০২৬ (BAJUS)',
    source: 'বাংলাদেশ জুয়েলার্স সমিতি (BAJUS) ঘোষিত দর',
    sourceUrl: 'https://www.bajus.org/gold-price',
    goldPerVori22k: 220858,
    silverPerVori22k: 3499,
    nisabGoldVori: 7.5,    // সাড়ে ৭ ভরি স্বর্ণ
    nisabSilverVori: 52.5, // সাড়ে ৫২ ভরি রুপা
    rate: 2.5,
    voriGram: 11.664
  },

  /* ---------- bKash / Nagad চার্জ ---------- */
  mfs: {
    checked: '৩ নভেম্বর ২০২৬',
    note: 'অফার ও চার্জ প্রায়ই বদলায়। লেনদেনের আগে অ্যাপে দেখানো চূড়ান্ত চার্জ মিলিয়ে নিন।',
    providers: {
      bkash: {
        name: 'বিকাশ', sourceUrl: 'https://www.bkash.com/en/products-services/cashout',
        services: [
          { id: 'co_agent', name: 'ক্যাশ আউট (সাধারণ এজেন্ট)', perThousand: 18.50 },
          { id: 'co_priyo', name: 'ক্যাশ আউট (প্রিয় এজেন্ট, মাসে ৫০,০০০ পর্যন্ত)', perThousand: 13.95 },
          { id: 'co_atm',   name: 'ক্যাশ আউট (ATM)', perThousand: 14.90 },
          { id: 'sm_priyo', name: 'সেন্ড মানি (প্রিয় নাম্বার, মাসে ২৫,০০০ পর্যন্ত)', flat: 0 },
          { id: 'sm_other', name: 'সেন্ড মানি (অন্য নাম্বার)', flat: 5, note: 'বিকাশের ওয়েবসাইট অনুযায়ী সীমার পরে ৳৫ (বড় অংকে ৳১০) — অ্যাপে মিলিয়ে নিন' }
        ]
      },
      nagad: {
        name: 'নগদ', sourceUrl: 'https://nagad.com.bd/',
        services: [
          { id: 'co_app',  name: 'ক্যাশ আউট (অ্যাপ)', perThousand: 14.90 },
          { id: 'co_ussd', name: 'ক্যাশ আউট (*167# USSD)', perThousand: 18.50 },
          { id: 'sm',      name: 'সেন্ড মানি', flat: 0, note: 'বর্তমানে ফ্রি বলে প্রকাশিত — অ্যাপে মিলিয়ে নিন' }
        ]
      }
    }
  }
};
