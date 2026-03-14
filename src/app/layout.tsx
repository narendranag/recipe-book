import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nag Family Recipes",
  description:
    "A curated collection of family recipes — from weeknight dinners to festive feasts.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@400;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen">
        <header className="border-b border-light-gray">
          <div className="max-w-6xl mx-auto px-4 py-6">
            <a href="/" className="block text-center">
              <h1 className="text-3xl md:text-4xl font-bold text-warm-black tracking-tight">
                Nag Family Recipes
              </h1>
              <p className="text-sm text-mid-gray mt-1 font-sans">
                A curated collection of family favorites
              </p>
            </a>
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-4 py-8">{children}</main>
        <footer className="border-t border-light-gray mt-16">
          <div className="max-w-6xl mx-auto px-4 py-8 text-center text-sm text-mid-gray">
            <p>Nag Family Recipes</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
