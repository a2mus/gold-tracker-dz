import type { Metadata } from "next";
import { Cairo } from "next/font/google";
import "./globals.css";

const cairo = Cairo({
  subsets: ["arabic", "latin"],
  variable: "--font-cairo",
});

export const metadata: Metadata = {
  title: "أسعار الذهب في الجزائر | Gold Tracker DZ",
  description: "تتبع أسعار الذهب اللحظية في الجزائر - 18 و 21 و 22 و 24 قيراط",
  keywords: ["ذهب", "الجزائر", "أسعار الذهب", "gold", "algeria", "prix or"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl">
      <body className={`${cairo.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
