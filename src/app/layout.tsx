import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OCR Document Processor",
  description: "AI-powered document processing with OCR and structured data extraction",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
/*add new File in this dummy*/