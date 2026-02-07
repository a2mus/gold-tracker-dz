"use client";

interface GoldCardProps {
  karat: string;
  price: number;
  change: number;
  isSelected?: boolean;
  onClick?: () => void;
}

export function GoldCard({ karat, price, change, isSelected, onClick }: GoldCardProps) {
  const isPositive = change >= 0;
  
  const karatLabels: Record<string, string> = {
    "24k": "24 قيراط",
    "22k": "22 قيراط",
    "21k": "21 قيراط",
    "18k": "18 قيراط",
  };

  return (
    <button
      onClick={onClick}
      className={`
        relative overflow-hidden rounded-2xl p-6 transition-all duration-300
        ${isSelected 
          ? "bg-gradient-to-br from-amber-500 to-yellow-600 shadow-lg shadow-amber-500/30 scale-105" 
          : "bg-slate-800/80 hover:bg-slate-700/80 border border-amber-500/20"
        }
      `}
    >
      {/* Gold shimmer effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -skew-x-12 animate-shimmer" />
      
      <div className="relative">
        <div className={`text-sm font-medium mb-2 ${isSelected ? "text-amber-100" : "text-amber-400"}`}>
          {karatLabels[karat] || karat}
        </div>
        
        <div className={`text-2xl md:text-3xl font-bold mb-2 ${isSelected ? "text-white" : "text-white"}`}>
          {price.toLocaleString("ar-DZ")}
        </div>
        
        <div className="text-xs text-slate-400 mb-2">
          دج / غرام
        </div>
        
        <div className={`
          inline-flex items-center gap-1 text-sm font-medium px-2 py-1 rounded-full
          ${isPositive 
            ? "bg-green-500/20 text-green-400" 
            : "bg-red-500/20 text-red-400"
          }
        `}>
          <span>{isPositive ? "▲" : "▼"}</span>
          <span>{Math.abs(change).toFixed(2)}%</span>
        </div>
      </div>
    </button>
  );
}
