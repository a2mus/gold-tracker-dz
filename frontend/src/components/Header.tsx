"use client";

import { useState, useEffect } from "react";

export function Header() {
  const [time, setTime] = useState<string>("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(now.toLocaleString("ar-DZ", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }));
    };
    
    updateTime();
    const interval = setInterval(updateTime, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="bg-slate-900/80 backdrop-blur-sm border-b border-amber-500/20 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-4xl">🪙</div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-amber-400">
                أسعار الذهب
              </h1>
              <p className="text-xs text-slate-400">الجزائر</p>
            </div>
          </div>
          
          <div className="text-left text-sm text-slate-400">
            <div className="hidden md:block">{time}</div>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-xs">مباشر</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
