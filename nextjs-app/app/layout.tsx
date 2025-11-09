import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'OCR Text Detection - EthnoSoul Legacy',
  description: 'Extract text from images and PDFs using AI OCR',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" className="scroll-smooth">
      <body className="font-lexend">{children}</body>
    </html>
  );
}
