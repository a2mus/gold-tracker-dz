import type { Metadata } from 'next'
import { Inter, Tajawal } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const tajawal = Tajawal({ subsets: ['arabic'], weight: ['400', '500', '700'], variable: '--font-tajawal' })

export const metadata: Metadata = {
  title: 'Gold Intelligence DZ - Tableau de Bord',
  description: 'Tableau de bord intelligent pour le suivi des cours de l\'or en Algérie et dans le monde.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr" dir="ltr" className="dark">
      <body className={`${inter.variable} ${tajawal.variable} bg-background-light dark:bg-background-dark text-gray-900 dark:text-gray-100 font-display min-h-screen flex flex-col antialiased transition-colors duration-300`}>
        {children}
      </body>
    </html>
  )
}
