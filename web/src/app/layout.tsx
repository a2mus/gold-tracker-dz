import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Gold Tracker Algeria | أسعار الذهب في الجزائر',
  description: 'تتبع أسعار الذهب في الجزائر في الوقت الفعلي - 18k, 21k, 22k, 24k | Real-time gold prices in Algeria',
  keywords: ['gold', 'algeria', 'prix or', 'ذهب', 'الجزائر', 'سعر الذهب', 'sabika', 'سبيكة'],
  openGraph: {
    title: 'Gold Tracker Algeria',
    description: 'أسعار الذهب في الجزائر',
    locale: 'ar_DZ',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
