"use client";

interface PriceChartProps {
  karat: string;
}

export function PriceChart({ karat }: PriceChartProps) {
  // Mock data - replace with real API data
  const data = [
    { date: "01/02", price: 18200 },
    { date: "02/02", price: 18350 },
    { date: "03/02", price: 18280 },
    { date: "04/02", price: 18420 },
    { date: "05/02", price: 18380 },
    { date: "06/02", price: 18450 },
    { date: "07/02", price: 18500 },
  ];

  const maxPrice = Math.max(...data.map(d => d.price));
  const minPrice = Math.min(...data.map(d => d.price));
  const range = maxPrice - minPrice || 1;

  return (
    <div className="h-64">
      <div className="flex items-end justify-between h-48 gap-2">
        {data.map((point, index) => {
          const height = ((point.price - minPrice) / range) * 100;
          return (
            <div key={index} className="flex-1 flex flex-col items-center gap-2">
              <div className="text-xs text-slate-400">
                {point.price.toLocaleString("ar-DZ")}
              </div>
              <div 
                className="w-full bg-gradient-to-t from-amber-600 to-amber-400 rounded-t-lg transition-all duration-500 hover:from-amber-500 hover:to-amber-300"
                style={{ height: `${Math.max(height, 10)}%` }}
              />
              <div className="text-xs text-slate-500">{point.date}</div>
            </div>
          );
        })}
      </div>
      
      <div className="mt-4 flex justify-between text-sm text-slate-400">
        <span>أقل: {minPrice.toLocaleString("ar-DZ")} دج</span>
        <span>أعلى: {maxPrice.toLocaleString("ar-DZ")} دج</span>
      </div>
    </div>
  );
}
