import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import computerIcon from '@/assets/computer-icon.gif';

export function VoiceOverlay() {
    const [isActive, setIsActive] = useState(false);
    const [status, setStatus] = useState('listening'); // listening, processing, speaking

    // WebSocket Connection
    useEffect(() => {
        let ws: WebSocket | null = null;
        let reconnectTimer: any = null;

        const connect = () => {
            try {
                ws = new WebSocket('ws://localhost:8000/ws');

                ws.onopen = () => {
                    console.log('Connected to Voice Assistant');
                };

                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        console.log('Voice Status:', data);

                        if (data.status === 'listening') {
                            setIsActive(true);
                            setStatus('listening');
                        } else if (data.status === 'processing') {
                            setIsActive(true);
                            setStatus('processing');
                        } else if (data.status === 'speaking') {
                            setIsActive(true);
                            setStatus('speaking');
                        } else if (data.status === 'idle') {
                            // Short delay before hiding to show "done" state if needed
                            setTimeout(() => setIsActive(false), 1000);
                        }
                    } catch (e) {
                        console.error('Error parsing WS message', e);
                    }
                };

                ws.onclose = () => {
                    console.log('Disconnected from Voice Assistant');
                    // Try reconnecting after 3 seconds
                    reconnectTimer = setTimeout(connect, 3000);
                };

                ws.onerror = (err) => {
                    console.error('WebSocket error', err);
                    ws?.close();
                };
            } catch (e) {
                console.error("Connection error:", e);
            }
        };

        connect();

        return () => {
            if (ws) ws.close();
            if (reconnectTimer) clearTimeout(reconnectTimer);
        };
    }, []);

    // Keyboard shortcut to toggle (Spacebar mock - keep for manual testing)
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.code === 'Space' && !e.repeat && !(e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement)) {
                e.preventDefault(); // Prevent scrolling
                setIsActive(prev => !prev);
                if (!isActive) setStatus('listening'); // Default to listening on manual toggle
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isActive]);

    // Helper to get text based on status
    const getStatusText = () => {
        switch (status) {
            case 'listening': return 'Listening...';
            case 'processing': return 'Thinking...';
            case 'speaking': return 'Speaking...';
            default: return 'Ready';
        }
    };

    return (
        <>
            <AnimatePresence>
                {isActive && (
                    <motion.div
                        initial={{ y: 100, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        exit={{ y: 100, opacity: 0 }}
                        transition={{ type: "spring", damping: 20, stiffness: 300 }}
                        className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-4 pointer-events-none"
                    >
                        {/* Listening Indicator */}
                        <motion.div
                            className="bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex flex-col items-center shadow-2xl"
                            initial={{ scale: 0.9 }}
                            animate={{ scale: 1 }}
                        >
                            <div className="relative w-32 h-32 flex items-center justify-center">
                                {/* Ripple Effect - Only show when listening or speaking */}
                                {(status === 'listening' || status === 'speaking') && [1, 2, 3].map((ring) => (
                                    <motion.div
                                        key={ring}
                                        className={`absolute inset-0 rounded-full border ${status === 'speaking' ? 'border-green-500' : 'border-[var(--accent-primary)]'}`}
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: [0, 0.5, 0], scale: 1.5 }}
                                        transition={{
                                            duration: status === 'speaking' ? 0.5 : 2, // Faster ripple when speaking
                                            repeat: Infinity,
                                            delay: ring * (status === 'speaking' ? 0.1 : 0.4),
                                            ease: "easeOut"
                                        }}
                                    />
                                ))}

                                {/* Processing Spinner */}
                                {status === 'processing' && (
                                    <motion.div
                                        className="absolute inset-0 rounded-full border-4 border-t-[var(--accent-primary)] border-r-transparent border-b-[var(--accent-primary)] border-l-transparent"
                                        animate={{ rotate: 360 }}
                                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                    />
                                )}

                                {/* The Icon */}
                                <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-[var(--accent-primary)] relative z-10 bg-black">
                                    <img
                                        src={computerIcon}
                                        alt="Voice Assistant"
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                            </div>

                            <div className="mt-4 flex flex-col items-center gap-1">
                                <span className="text-white font-medium text-lg tracking-wide">{getStatusText()}</span>
                                {(status === 'listening') && <span className="text-white/50 text-xs uppercase tracking-wider">Speak Now</span>}
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Trigger Hint (Temporary for Demo) */}
            {!isActive && (
                <div className="fixed bottom-4 left-1/2 -translate-x-1/2 text-xs text-white/30 pointer-events-none">
                    Press [Space] to talk
                </div>
            )}
        </>
    );
}
