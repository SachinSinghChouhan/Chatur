import { Hero } from '@/app/components/Hero';
import { HowItWorks } from '@/app/components/HowItWorks';
import { Features } from '@/app/components/Features';
import { BilingualDemo } from '@/app/components/BilingualDemo';
import { DeveloperSection } from '@/app/components/DeveloperSection';
import { DownloadCTA } from '@/app/components/DownloadCTA';
import { Footer } from '@/app/components/Footer';
import { MotionProvider } from '@/app/components/motion-config';
import { Navigation } from '@/app/components/Navigation';

export default function App() {
  return (
    <MotionProvider>
      <div className="min-h-screen" style={{ backgroundColor: 'var(--background)' }}>
        <Navigation />
        <Hero />
        <div id="features">
          <HowItWorks />
          <Features />
        </div>
        <div id="demo">
          <BilingualDemo />
        </div>
        <div id="developers">
          <DeveloperSection />
        </div>
        <DownloadCTA />
        <Footer />
      </div>
    </MotionProvider>
  );
}