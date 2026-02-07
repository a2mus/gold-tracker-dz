"use client";

import { useState, useEffect } from "react";
import { GoldCard } from "@/components/GoldCard";
import { PriceChart } from "@/components/PriceChart";
import { Header } from "@/components/Header";

interface Prices {
  "24k": number;
  "22k": number;
  "21k": number;
  "18k": number;
}

interface PriceData {
  timestamp: string;
  prices: Prices;
  change_24h: Record<string, number>;
}

export default function Home() {
  const [prices, setPrices] = useState<PriceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedKarat, setSelectedKarat] = useState<string>("24k");

  useEffect(() => {
    // Mock data for now - replace with API call
    setPrices({
      timestamp: new Date().toISOString(),
      prices: {
        "24k": 18500,
        "22k": 17000,
        "21k": 16200,
        "18k": 13900,
      },
      change_24h: {
        "24k": 0.5,
        "22k": 0.3,
        "21k": 0.4,
        "18k": 0.2,
      },
    });
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-900 via-yellow-800 to-amber-700 flex items-center justify-center">
        <div className="text-white text-2xl animate-pulse">جاري التحميل...</div>
      </div>
    );
  }

  const karats = ["24k", "22k", "21k", "18k"] as const;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Current Prices Grid */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-amber-400 mb-6 text-center">
            أسعار الذهب اليوم
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {karats.map((karat) => (
              <GoldCard
                key={karat}
                karat={karat}
                price={prices?.prices[karat] || 0}
                change={prices?.change_24h[karat] || 0}
                isSelected={selectedKarat === karat}
                onClick={() => setSelectedKarat(karat)}
              />
            ))}
          </div>
        </section>

        {/* Price Chart */}
        <section className="mb-12">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-amber-500/20">
            <h2 className="text-xl font-bold text-amber-400 mb-4">
              تطور الأسعار - {selectedKarat}
            </h2>
            <PriceChart karat={selectedKarat} />
          </div>
        </section>

        {/* Info Section */}
        <section className="grid md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-amber-500/20">
            <h3 className="text-lg font-bold text-amber-400 mb-4">عن الخدمة</h3>
            <p className="text-slate-300 text-sm leading-relaxed">
              نوفر لكم أسعار الذهب المحدثة يومياً من مصادر موثوقة في السوق الجزائري.
              الأسعار تشمل جميع العيارات الشائعة (18، 21، 22، 24 قيراط) بالدينار الجزائري للغرام الواحد.
            </p>
          </div>
          
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-amber-500/20">
            <h3 className="text-lg font-bold text-amber-400 mb-4">المصدر</h3>
            <p className="text-slate-300 text-sm leading-relaxed">
              الأسعار مستخرجة من قناة{" "}
              <a 
                href="https://t.me/bijouteriechalabi" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-amber-400 hover:text-amber-300 underline"
              >
                مجوهرات شلابي
              </a>
              {" "}على تيليجرام.
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700 mt-12 py-6">
        <div className="container mx-auto px-4 text-center text-slate-500 text-sm">
          <p>© 2026 Gold Tracker DZ - Nexus DZ Labs</p>
        </div>
      </footer>
    </div>
  );
}
