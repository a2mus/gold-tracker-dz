'use client'

import { useState, useEffect } from 'react'
import { TrendingUp, TrendingDown, RefreshCw, Bell, Globe } from 'lucide-react'

// Types
interface PriceSummary {
  karat: number
  current_price: number
  change_24h: number | null
  change_percent: number | null
  high_24h: number | null
  low_24h: number | null
  last_updated: string
}

interface WorldPrice {
  price_usd: number
  price_dzd: number
  premium_percent: number
}

// Mock data for initial display
const mockPrices: PriceSummary[] = [
  { karat: 18, current_price: 29700, change_24h: 100, change_percent: 0.34, high_24h: 29800, low_24h: 29500, last_updated: new Date().toISOString() },
  { karat: 21, current_price: 34650, change_24h: 150, change_percent: 0.43, high_24h: 34800, low_24h: 34400, last_updated: new Date().toISOString() },
  { karat: 22, current_price: 36300, change_24h: -200, change_percent: -0.55, high_24h: 36500, low_24h: 36000, last_updated: new Date().toISOString() },
  { karat: 24, current_price: 39600, change_24h: 250, change_percent: 0.63, high_24h: 39800, low_24h: 39300, last_updated: new Date().toISOString() },
]

const karatLabels: Record<number, string> = {
  18: 'ذهب 18 قيراط',
  21: 'ذهب 21 قيراط',
  22: 'ذهب 22 قيراط',
  24: 'ذهب 24 قيراط (صافي)',
}

function formatPrice(price: number): string {
  return new Intl.NumberFormat('ar-DZ').format(price) + ' دج'
}

function formatPercent(percent: number | null): string {
  if (percent === null) return '--'
  const sign = percent >= 0 ? '+' : ''
  return `${sign}${percent.toFixed(2)}%`
}

function PriceCard({ price }: { price: PriceSummary }) {
  const isUp = (price.change_24h ?? 0) >= 0
  
  return (
    <div className="card glow-gold hover:scale-[1.02] transition-transform duration-300">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg text-slate-400">{karatLabels[price.karat]}</h3>
          <div className="text-3xl font-bold text-white mt-1">
            {formatPrice(price.current_price)}
          </div>
        </div>
        <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold ${
          isUp ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
        }`}>
          {isUp ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
          {formatPercent(price.change_percent)}
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-slate-500">أعلى 24س</span>
          <div className="text-slate-300">{price.high_24h ? formatPrice(price.high_24h) : '--'}</div>
        </div>
        <div>
          <span className="text-slate-500">أدنى 24س</span>
          <div className="text-slate-300">{price.low_24h ? formatPrice(price.low_24h) : '--'}</div>
        </div>
      </div>
    </div>
  )
}

function WorldPriceCard({ worldPrice }: { worldPrice: WorldPrice }) {
  return (
    <div className="card border-gold-500/30">
      <div className="flex items-center gap-2 mb-4">
        <Globe className="text-gold-400" size={24} />
        <h3 className="text-lg text-slate-300">السعر العالمي</h3>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        <div>
          <span className="text-slate-500 text-sm">بالدولار</span>
          <div className="text-xl font-bold text-gold-400">${worldPrice.price_usd.toFixed(2)}</div>
        </div>
        <div>
          <span className="text-slate-500 text-sm">بالدينار</span>
          <div className="text-xl font-bold text-white">{formatPrice(worldPrice.price_dzd)}</div>
        </div>
        <div>
          <span className="text-slate-500 text-sm">علاوة الجزائر</span>
          <div className="text-xl font-bold text-amber-400">+{worldPrice.premium_percent}%</div>
        </div>
      </div>
    </div>
  )
}

export default function Home() {
  const [prices, setPrices] = useState<PriceSummary[]>(mockPrices)
  const [worldPrice, setWorldPrice] = useState<WorldPrice>({ price_usd: 2850.50, price_dzd: 39600, premium_percent: 2.3 })
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [loading, setLoading] = useState(false)

  const refreshData = async () => {
    setLoading(true)
    try {
      // TODO: Fetch from API
      // const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/dashboard`)
      // const data = await response.json()
      // setPrices(data.prices)
      // setWorldPrice(data.world_price)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Failed to fetch prices:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // Auto-refresh every 5 minutes
    const interval = setInterval(refreshData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <main className="min-h-screen px-4 py-8 md:px-8 lg:px-16">
      {/* Header */}
      <header className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gold-gradient">أسعار الذهب في الجزائر</span>
        </h1>
        <p className="text-slate-400 text-lg">
          تتبع أسعار الذهب المحلية في الوقت الفعلي
        </p>
        
        <div className="flex items-center justify-center gap-4 mt-6">
          <button
            onClick={refreshData}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-gold-500/20 text-gold-400 rounded-lg hover:bg-gold-500/30 transition-colors disabled:opacity-50"
          >
            <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
            تحديث
          </button>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-slate-700/50 text-slate-300 rounded-lg hover:bg-slate-700 transition-colors">
            <Bell size={18} />
            تنبيهات
          </button>
        </div>
        
        <p className="text-slate-500 text-sm mt-4">
          آخر تحديث: {lastUpdate.toLocaleTimeString('ar-DZ')}
        </p>
      </header>

      {/* World Price */}
      <section className="max-w-4xl mx-auto mb-8">
        <WorldPriceCard worldPrice={worldPrice} />
      </section>

      {/* Price Grid */}
      <section className="max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-white mb-6">الأسعار المحلية</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {prices.map((price) => (
            <PriceCard key={price.karat} price={price} />
          ))}
        </div>
      </section>

      {/* Sabika Section */}
      <section className="max-w-4xl mx-auto mt-12">
        <div className="card border-gold-600/30 bg-gradient-to-br from-gold-900/20 to-slate-800/50">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-4xl">🥇</span>
            <div>
              <h3 className="text-xl font-bold text-gold-400">سعر السبيكة (750)</h3>
              <p className="text-slate-400">ذهب 18 قيراط - وزن 4 غرام</p>
            </div>
          </div>
          <div className="text-4xl font-bold text-white">
            {formatPrice(29700 * 4)}
          </div>
          <p className="text-slate-500 mt-2">≈ 4 × سعر الغرام 18k</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center mt-16 py-8 border-t border-slate-800">
        <p className="text-slate-500 text-sm">
          Gold Tracker Algeria - جزء من Nexus-DZ Labs
        </p>
        <p className="text-slate-600 text-xs mt-2">
          البيانات للإشارة فقط - ليست نصيحة استثمارية
        </p>
      </footer>
    </main>
  )
}
