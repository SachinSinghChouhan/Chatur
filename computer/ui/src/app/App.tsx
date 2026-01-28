import React, { useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { Hero } from '@/app/components/Hero';
import { HowItWorks } from '@/app/components/HowItWorks';
import { Features } from '@/app/components/Features';
import { BilingualDemo } from '@/app/components/BilingualDemo';
import { DeveloperSection } from '@/app/components/DeveloperSection';
import { DownloadCTA } from '@/app/components/DownloadCTA';
import { Footer } from '@/app/components/Footer';
import { MotionProvider } from '@/app/components/motion-config';
import { Navigation } from '@/app/components/Navigation';
import { LoadingScreen } from '@/app/components/LoadingScreen';
import { VoiceOverlay } from '@/app/components/VoiceOverlay';
import { SettingsModal } from '@/app/components/SettingsModal';
import { OnboardingWizard } from '@/app/components/OnboardingWizard';
import { Settings } from 'lucide-react';
import { Button } from '@/app/components/ui/button';

export default function App() {
  const [loading, setLoading] = useState(true);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [wizardOpen, setWizardOpen] = useState(false);

  // Check onboarding status on load
  React.useEffect(() => {
    if (!loading) {
      const completed = localStorage.getItem('onboarding_complete');
      if (!completed) {
        // Short delay to allow loading animations to settle
        setTimeout(() => setWizardOpen(true), 1500);
      }
    }
  }, [loading]);

  return (
    <MotionProvider>
      <div className="min-h-screen relative" style={{ backgroundColor: 'var(--background)' }}>

        <AnimatePresence mode="wait">
          {loading ? (
            <LoadingScreen key="loader" onComplete={() => setLoading(false)} />
          ) : (
            <motion.div
              key="main-content"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8 }}
            >
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
            </motion.div>
          )}
        </AnimatePresence>

        <VoiceOverlay />

        {/* Settings Floating Button */}
        {!loading && (
          <div className="fixed bottom-6 right-6 z-40">
            <Button
              variant="outline"
              size="icon"
              className="rounded-full w-12 h-12 bg-black/50 backdrop-blur-md border-white/10 hover:bg-white/10 text-white shadow-lg"
              onClick={() => setSettingsOpen(true)}
            >
              <Settings className="w-5 h-5" />
            </Button>
          </div>
        )}

        <SettingsModal open={settingsOpen} onOpenChange={setSettingsOpen} />
        <OnboardingWizard open={wizardOpen} onComplete={() => setWizardOpen(false)} />
      </div>
    </MotionProvider>
  );
}