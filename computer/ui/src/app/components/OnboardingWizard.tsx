import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Dialog, DialogContent } from '@/app/components/ui/dialog';
import { Button } from '@/app/components/ui/button';
import { CheckCircle2, Mic, ArrowRight, Server, Wifi } from 'lucide-react';
import computerIcon from '@/assets/computer-icon.gif';

interface OnboardingWizardProps {
    open: boolean;
    onComplete: () => void;
}

export function OnboardingWizard({ open, onComplete }: OnboardingWizardProps) {
    const [step, setStep] = useState(1);
    const [isConnected, setIsConnected] = useState(false);
    const [isChecking, setIsChecking] = useState(false);

    const checkConnection = async () => {
        setIsChecking(true);
        try {
            const res = await fetch('http://localhost:8000/status');
            if (res.ok) {
                setIsConnected(true);
                setTimeout(() => setStep(3), 1000); // Auto advance
            }
        } catch (e) {
            setIsConnected(false);
        } finally {
            setIsChecking(false);
        }
    };

    const handleComplete = () => {
        localStorage.setItem('onboarding_complete', 'true');
        onComplete();
    };

    return (
        <Dialog open={open} onOpenChange={() => { }}>
            <DialogContent className="sm:max-w-[600px] h-[400px] bg-zinc-950 border-zinc-800 text-zinc-100 flex flex-col items-center justify-center text-center p-0 overflow-hidden [&>button]:hidden">
                {/* Background ambient glow */}
                <div className="absolute inset-0 bg-gradient-to-tr from-[var(--accent-primary)]/10 via-transparent to-transparent pointer-events-none" />

                <AnimatePresence mode="wait">
                    {step === 1 && (
                        <motion.div
                            key="step1"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="flex flex-col items-center gap-6 p-8 relative z-10"
                        >
                            <div className="w-24 h-24 rounded-full border-2 border-[var(--accent-primary)] overflow-hidden shadow-[0_0_30px_rgba(var(--accent-primary-rgb),0.3)]">
                                <img src={computerIcon} alt="Computer" className="w-full h-full object-cover" />
                            </div>
                            <div className="space-y-2">
                                <h2 className="text-3xl font-bold tracking-tight">Hello, I am Computer.</h2>
                                <p className="text-zinc-400 max-w-sm mx-auto">
                                    I am your voice-controlled AI assistant. I can help you manage your tasks, control your media, and find information.
                                </p>
                            </div>
                            <Button
                                onClick={() => setStep(2)}
                                className="mt-4 bg-[var(--accent-primary)] text-black hover:bg-[var(--accent-primary)]/90 px-8 rounded-full"
                            >
                                Get Started <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>
                        </motion.div>
                    )}

                    {step === 2 && (
                        <motion.div
                            key="step2"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 1.05 }}
                            className="flex flex-col items-center gap-6 p-8 relative z-10 w-full"
                        >
                            <div className="w-16 h-16 rounded-full bg-zinc-900 flex items-center justify-center border border-zinc-800">
                                {isChecking ? (
                                    <motion.div
                                        animate={{ rotate: 360 }}
                                        transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                                    >
                                        <Server className="w-8 h-8 text-zinc-500" />
                                    </motion.div>
                                ) : isConnected ? (
                                    <CheckCircle2 className="w-8 h-8 text-green-500" />
                                ) : (
                                    <Wifi className="w-8 h-8 text-zinc-500" />
                                )}
                            </div>

                            <div className="space-y-2">
                                <h2 className="text-2xl font-semibold">Connecting to System...</h2>
                                <p className="text-zinc-400">
                                    Checking connection to the voice engine.
                                </p>
                            </div>

                            {!isConnected && (
                                <Button
                                    onClick={checkConnection}
                                    className="bg-zinc-100 text-zinc-900 hover:bg-zinc-200"
                                    disabled={isChecking}
                                >
                                    {isChecking ? 'Checking...' : 'Check Connection'}
                                </Button>
                            )}

                            {isConnected && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                                    <p className="text-green-500 font-medium">Connected successfully!</p>
                                </motion.div>
                            )}
                        </motion.div>
                    )}

                    {step === 3 && (
                        <motion.div
                            key="step3"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="flex flex-col items-center gap-8 p-8 relative z-10"
                        >
                            <div className="grid grid-cols-2 gap-4 w-full max-w-md">
                                <div className="bg-zinc-900/50 p-4 rounded-xl border border-white/5 flex flex-col items-center text-center gap-2">
                                    <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                                        <Mic className="w-5 h-5 text-zinc-300" />
                                    </div>
                                    <h3 className="font-medium text-white">Voice Control</h3>
                                    <p className="text-xs text-zinc-400">Just speak naturally. "What's the weather?"</p>
                                </div>
                                <div className="bg-zinc-900/50 p-4 rounded-xl border border-white/5 flex flex-col items-center text-center gap-2">
                                    <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                                        <span className="font-mono font-bold text-zinc-300">Space</span>
                                    </div>
                                    <h3 className="font-medium text-white">Quick Trigger</h3>
                                    <p className="text-xs text-zinc-400">Press Spacebar to toggle listening manually.</p>
                                </div>
                            </div>

                            <Button
                                onClick={handleComplete}
                                className="bg-[var(--accent-primary)] text-black hover:bg-[var(--accent-primary)]/90 px-10 rounded-full text-lg h-12"
                            >
                                I'm Ready
                            </Button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </DialogContent>
        </Dialog>
    );
}
