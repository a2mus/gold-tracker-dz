'use client';

import React, { useEffect, useState } from 'react';
import { 
  Bell, 
  Newspaper, 
  PlusCircle, 
  Crown, 
  Lightbulb, 
  TrendingUp, 
  Brain, 
  Table as TableIcon, 
  Hammer, 
  Diamond, 
  Coins, 
  PiggyBank, 
  Globe 
} from 'lucide-react';
import { AreaChart, Area, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

// Data for the chart
const chartData = [
  { name: 'Nov 01', local: 20000, global: 19000 },
  { name: 'Nov 05', local: 20200, global: 19200 },
  { name: 'Nov 10', local: 20100, global: 19400 },
  { name: 'Nov 15', local: 20800, global: 19800 },
  { name: 'Nov 20', local: 20600, global: 19500 },
  { name: 'Nov 25', local: 21000, global: 19300 },
  { name: 'Nov 30', local: 21500, global: 19600 },
];

export default function Dashboard() {
  const [needleRotation, setNeedleRotation] = useState(45);

  useEffect(() => {
    // Animate needle on mount
    const timer = setTimeout(() => {
      setNeedleRotation(125);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="bg-background-light dark:bg-background-dark text-gray-900 dark:text-gray-100 font-display min-h-screen flex flex-col antialiased transition-colors duration-300">
      {/* Header */}
      <header className="h-16 border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark flex items-center justify-between px-6 sticky top-0 z-50">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary text-black font-bold h-10 w-10 flex items-center justify-center rounded-lg shadow-lg shadow-primary/20">
              DZ
            </div>
            <div>
              <h1 className="font-bold text-lg tracking-tight">Gold Intelligence</h1>
              <p className="text-xs text-text-muted-light dark:text-text-muted-dark">Algérie & Marché Mondial</p>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-4 ml-6 text-sm">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-background-light dark:bg-black/30 border border-border-light dark:border-border-dark">
              <span className="text-text-muted-light dark:text-text-muted-dark font-mono">1€ =</span>
              <span className="font-semibold text-primary">243.5 DZD</span>
              <span className="text-xs text-secondary bg-secondary/10 px-1 rounded">+0.2%</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-background-light dark:bg-black/30 border border-border-light dark:border-border-dark">
              <span className="text-text-muted-light dark:text-text-muted-dark font-mono">Or (Oz)</span>
              <span className="font-semibold text-primary">$2,038.10</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors relative">
            <Bell className="w-6 h-6 text-gray-600 dark:text-gray-400" />
            <span className="absolute top-2 right-2 h-2 w-2 bg-primary rounded-full animate-pulse"></span>
          </button>
          <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-gray-700 to-gray-600 flex items-center justify-center text-xs font-bold text-white cursor-pointer">
            A
          </div>
        </div>
      </header>

      <main className="flex-1 p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-[1920px] mx-auto w-full">
        {/* Sidebar */}
        <aside className="lg:col-span-3 space-y-4 flex flex-col">
          {/* News Feed */}
          <div className="bg-surface-light dark:bg-surface-dark rounded-xl p-4 border border-border-light dark:border-border-dark shadow-sm flex-1">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-sm uppercase tracking-wider text-text-muted-light dark:text-text-muted-dark flex items-center gap-2">
                <Newspaper className="text-primary text-base w-5 h-5" /> Actualités du Marché
              </h2>
              <span className="h-2 w-2 bg-secondary rounded-full animate-ping"></span>
            </div>
            <div className="space-y-4 overflow-y-auto max-h-[800px] pr-2">
              <NewsItem 
                initials="BE" 
                color="bg-gray-700" 
                title="Bijouterie El Aurassi" 
                time="12 min"
                content="Mise à jour importante : Le marché local montre des signes de résistance à 19,180 DZD. Forte demande anticipée pour la fin de semaine."
              />
              <NewsItem 
                initials="SQ" 
                color="bg-blue-900" 
                title="Square Official News" 
                time="45 min"
                content="Analyse technique : Le gap entre le taux parallèle et officiel se resserre légèrement. Impact direct sur le prix de l'or importé."
              />
              <NewsItem 
                initials="GM" 
                color="bg-yellow-700" 
                title="Assoc. Gold Merchants" 
                time="2h"
                content="Attention aux contrefaçons signalées dans la région Ouest. Vérifiez les poinçons avant tout achat majeur."
              />
              <NewsItem 
                initials="SX" 
                color="bg-green-800" 
                title="Setif Gold Exchange" 
                time="3h"
                content="Volume des transactions en hausse de 15% ce matin. Le sentiment général est haussier."
              />
            </div>
            <div className="mt-4 pt-4 border-t border-border-light dark:border-border-dark">
              <button className="w-full py-2 bg-primary text-black font-semibold rounded-lg hover:bg-primary/90 transition-colors text-sm flex items-center justify-center gap-2 shadow-lg shadow-primary/20">
                <PlusCircle className="text-lg w-5 h-5" /> Nouvelle Source
              </button>
            </div>
          </div>

          {/* Premium Ad */}
          <div className="bg-gradient-to-br from-gray-800 to-black rounded-xl p-5 border border-border-light dark:border-border-dark shadow-sm relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
              <Crown className="text-6xl text-primary w-16 h-16" />
            </div>
            <h3 className="text-primary text-xs font-bold uppercase tracking-widest mb-1">Partenaire Premium</h3>
            <h2 className="text-white font-bold text-lg mb-2">Service VIP Lingots</h2>
            <p className="text-gray-400 text-xs mb-3">Sécurisez vos investissements avec notre service de garde sécurisé.</p>
            <button className="text-white text-xs border border-white/30 hover:bg-white/10 px-3 py-1.5 rounded transition-colors">En savoir plus</button>
          </div>
        </aside>

        {/* Main Content */}
        <div className="lg:col-span-9 space-y-6">
          {/* AI Analysis Section */}
          <div className="bg-surface-light dark:bg-surface-dark rounded-xl p-6 border border-border-light dark:border-border-dark shadow-sm relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full filter blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative z-10">
              <div className="flex-1">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                  Analyse IA (AI Rationale) <span className="px-2 py-0.5 rounded text-[10px] bg-primary/20 text-primary border border-primary/30">BETA</span>
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed max-w-2xl">
                  L'algorithme a analysé 142 points de données. La tendance suggère une hausse modérée due à l'incertitude sur le marché des devises parallèles. La cassure du niveau de résistance S1 (19,200) pourrait déclencher un mouvement haussier significatif.
                </p>
                <div className="flex gap-4 mt-6">
                  <div className="bg-background-light dark:bg-background-dark/60 rounded-lg p-3 border border-border-light dark:border-border-dark flex items-center gap-3 min-w-[180px]">
                    <Lightbulb className="text-primary w-6 h-6" />
                    <div>
                      <div className="text-[10px] text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide">Prévision 24h</div>
                      <div className="font-semibold text-sm dark:text-gray-200">Test de la résistance</div>
                    </div>
                  </div>
                  <div className="bg-background-light dark:bg-background-dark/60 rounded-lg p-3 border border-border-light dark:border-border-dark flex items-center gap-3 min-w-[180px]">
                    <TrendingUp className="text-secondary w-6 h-6" />
                    <div>
                      <div className="text-[10px] text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide">Signal</div>
                      <div className="font-semibold text-sm text-secondary">Achat Faible</div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex flex-col items-center">
                <div className="mb-2 text-xs font-medium text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider flex items-center gap-1">
                  <Brain className="text-sm w-4 h-4" /> Sentiment
                </div>
                <div className="gauge-container">
                  <div className="gauge-bg"></div>
                  <div 
                    className="gauge-needle" 
                    style={{ transform: `rotate(${needleRotation}deg)` }}
                  ></div>
                </div>
                <div className="flex justify-between w-[160px] text-[10px] font-bold mt-2 px-1">
                  <span className="text-danger">Vendre</span>
                  <span className="text-secondary">Acheter Fort</span>
                </div>
              </div>
            </div>
          </div>

          {/* Price Matrix */}
          <div className="bg-surface-light dark:bg-surface-dark rounded-xl border border-border-light dark:border-border-dark shadow-sm overflow-hidden">
            <div className="p-4 border-b border-border-light dark:border-border-dark flex justify-between items-center">
              <h2 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <TableIcon className="text-primary text-base w-5 h-5" /> Matrice des Prix (7 Jours)
              </h2>
              <span className="px-2 py-1 bg-secondary/10 text-secondary text-xs rounded border border-secondary/20 flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-secondary animate-pulse"></span> Live
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-background-light dark:bg-black/20 text-xs uppercase text-text-muted-light dark:text-text-muted-dark font-medium border-b border-border-light dark:border-border-dark">
                    <th className="p-4 font-semibold">Produit / Type</th>
                    <th className="p-4 font-semibold text-right">Prix Moyen (DA)</th>
                    <th className="p-4 font-semibold text-center">Tendance (1g)</th>
                    <th className="p-4 font-semibold text-right">Var. %</th>
                    <th className="p-4 font-semibold text-center">Statut</th>
                  </tr>
                </thead>
                <tbody className="text-sm divide-y divide-border-light dark:divide-border-dark">
                  <TableRow 
                    icon={<Hammer className="text-lg w-5 h-5" />} 
                    color="text-yellow-500" 
                    bg="bg-yellow-900/30"
                    title="Or Cassé (Local)" 
                    subtitle="18 Carats - Occasion" 
                    price="12,250" 
                    change="+0.85%" 
                    status="Haussier" 
                    trendColor="stroke-secondary"
                  />
                  <TableRow 
                    icon={<Diamond className="text-lg w-5 h-5" />} 
                    color="text-blue-400" 
                    bg="bg-blue-900/30"
                    title="Importé (Italien)" 
                    subtitle="18 Carats - Neuf" 
                    price="14,300" 
                    change="0.00%" 
                    status="Stable" 
                    trendColor="stroke-gray-500"
                    trendPath="M0,15 L100,15"
                    statusColor="text-yellow-500 bg-yellow-500/10 border-yellow-500/20"
                    changeColor="text-gray-500"
                  />
                  <TableRow 
                    icon={<Crown className="text-lg w-5 h-5" />} 
                    color="text-orange-400" 
                    bg="bg-orange-900/30"
                    title="Local (Algérien)" 
                    subtitle="21 Carats - Artisanal" 
                    price="15,800" 
                    change="+1.15%" 
                    status="Actif" 
                    trendColor="stroke-secondary"
                  />
                  <TableRow 
                    icon={<Coins className="text-lg w-5 h-5" />} 
                    color="text-purple-400" 
                    bg="bg-purple-900/30"
                    title="Louis d'Or" 
                    subtitle="22 Carats - Pièce" 
                    price="68,500" 
                    change="-0.44%" 
                    status="Baisse" 
                    trendColor="stroke-danger"
                    trendPath="M0,5 C20,5 40,10 60,20 C80,25 90,28 100,28"
                    statusColor="text-danger bg-danger/10 border-danger/20"
                    changeColor="text-danger"
                  />
                  <TableRow 
                    icon={<PiggyBank className="text-lg w-5 h-5" />} 
                    color="text-amber-500" 
                    bg="bg-amber-900/30"
                    title="Lingot (Bullion)" 
                    subtitle="24 Carats - Brut" 
                    price="18,100" 
                    change="+2.2%" 
                    status="Forte Demande" 
                    trendColor="stroke-primary"
                    statusColor="text-primary bg-primary/10 border-primary/20"
                    changeColor="text-primary"
                  />
                </tbody>
              </table>
            </div>
          </div>

          {/* Chart Section */}
          <div className="bg-surface-light dark:bg-surface-dark rounded-xl p-6 border border-border-light dark:border-border-dark shadow-sm">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 gap-4">
              <div>
                <h2 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-1">
                  <Globe className="text-primary w-5 h-5" /> Comparatif: Marché Algérien vs Marché Spot
                </h2>
                <p className="text-xs text-text-muted-light dark:text-text-muted-dark">
                  Analyse du "Premium/Discount" (Écart de prix) entre l'or physique local et le cours mondial spot.
                </p>
              </div>
              <div className="flex gap-4 text-xs font-medium">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-primary"></span>
                  <span className="text-gray-600 dark:text-gray-400">Prix Moyen Local</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-secondary border border-secondary dashed"></span>
                  <span className="text-gray-600 dark:text-gray-400">Prix Mondial (Ajusté)</span>
                </div>
                <div className="px-2 py-1 bg-background-light dark:bg-background-dark border border-border-light dark:border-border-dark rounded text-text-muted-light dark:text-text-muted-dark">
                  Spread: <span className="text-green-500 font-bold">+12.5%</span>
                </div>
              </div>
            </div>
            <div className="relative w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorGold" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FBBF24" stopOpacity={0.5}/>
                      <stop offset="95%" stopColor="#FBBF24" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(26, 26, 26, 0.9)', border: '1px solid #333', borderRadius: '8px', color: '#fff' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="local" 
                    stroke="#FBBF24" 
                    strokeWidth={3}
                    fillOpacity={1} 
                    fill="url(#colorGold)" 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="global" 
                    stroke="#10B981" 
                    strokeWidth={2}
                    strokeDasharray="5 5" 
                    dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-auto py-6 border-t border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark text-center">
        <p className="text-xs text-text-muted-light dark:text-text-muted-dark mb-1">
          © 2023 Gold Intelligence DZ. Tous droits réservés.
        </p>
        <p className="text-[10px] text-gray-500 dark:text-gray-600 max-w-3xl mx-auto px-4">
          Les données sont fournies à titre informatif uniquement et ne constituent pas un conseil financier. Les prix du marché parallèle peuvent varier considérablement selon la région et le négociant.
        </p>
      </footer>
    </div>
  );
}

function NewsItem({ initials, color, title, time, content }: any) {
  return (
    <div className="p-3 rounded-lg bg-background-light dark:bg-background-dark/50 hover:bg-gray-100 dark:hover:bg-background-dark transition-colors border-l-2 border-transparent hover:border-primary cursor-pointer group">
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          <div className={`h-6 w-6 rounded ${color} flex items-center justify-center text-[10px] font-bold text-white`}>{initials}</div>
          <span className="text-xs font-semibold text-gray-700 dark:text-gray-300">{title}</span>
        </div>
        <span className="text-[10px] text-text-muted-light dark:text-text-muted-dark">{time}</span>
      </div>
      <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed group-hover:text-gray-900 dark:group-hover:text-gray-200">
        {content}
      </p>
    </div>
  );
}

function TableRow({ 
  icon, color, bg, title, subtitle, price, change, status, 
  trendColor, trendPath = "M0,25 C10,25 20,20 30,22 C40,24 50,15 60,10 C70,5 80,8 100,2",
  statusColor = "text-secondary bg-secondary/10 border-secondary/20",
  changeColor = "text-secondary"
}: any) {
  return (
    <tr className="hover:bg-background-light dark:hover:bg-white/5 transition-colors group">
      <td className="p-4">
        <div className="flex items-center gap-3">
          <div className={`p-2 ${bg} ${color} rounded-lg`}>
            {icon}
          </div>
          <div>
            <div className="font-semibold text-gray-900 dark:text-gray-100">{title}</div>
            <div className="text-xs text-text-muted-light dark:text-text-muted-dark">{subtitle}</div>
          </div>
        </div>
      </td>
      <td className="p-4 text-right font-mono font-bold text-gray-900 dark:text-white text-lg">{price}</td>
      <td className="p-4 text-center">
        <div className="w-24 h-8 mx-auto">
          <svg className={`w-full h-full ${trendColor} fill-none stroke-2`} viewBox="0 0 100 30">
            <path d={trendPath}></path>
          </svg>
        </div>
      </td>
      <td className={`p-4 text-right font-mono ${changeColor} font-medium`}>{change}</td>
      <td className="p-4 text-center">
        <span className={`px-2 py-1 rounded text-xs font-medium border ${statusColor}`}>
          {status}
        </span>
      </td>
    </tr>
  );
}
