import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import computerIcon from '@/assets/computer-icon.gif';

const WS_URL = 'ws://localhost:8000/ws';
const RECONNECT_DELAY_MS = 3000;
const HIDE_DELAY_MS = 1000;

type Status = 'listening' | 'processing' | 'speaking';

const statusText: Record<Status, string> = {
    listening: 'Listening...',
    processing: 'Thinking...',
    speaking: 'Speaking...',
};

export function VoiceOverlay() {
    const [isActive, setIsActive] = useState(false);
    const [status, setStatus] = useState<Status>('listening');

    useEffect(() => {
        let ws: WebSocket | null = null;
        let reconnectTimer: number | undefined;

        const connect = () => {
            try {
                ws = new WebSocket(WS_URL);

                ws.onopen = () => {
                    console.log('Connected to Voice Assistant');
                };

                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        const nextStatus = data?.status;

                        if (nextStatus === 'idle') {
                            window.setTimeout(() => setIsActive(false), HIDE_DELAY_MS);
                            return;
                        }

                        if (nextStatus === 'listening' || nextStatus === 'processing' || nextStatus === 'speaking') {
                            setIsActive(true);
                            setStatus(nextStatus);
                        }
                    } catch (error) {
                        console.error('Error parsing WS message', error);
                    }
                };

                ws.onclose = () => {
                    console.log('Disconnected from Voice Assistant');
                    reconnectTimer = window.setTimeout(connect, RECONNECT_DELAY_MS);
                };

                ws.onerror = (error) => {
                    console.error('WebSocket error', error);
                    ws?.close();
                };
            } catch (error) {
                console.error('Connection error:', error);
            }
        };

        connect();

        return () => {
            ws?.close();
            if (reconnectTimer) {
                window.clearTimeout(reconnectTimer);
            }
        };
    }, []);

    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            const isInput = event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement;
            if (event.code === 'Space' && !event.repeat && !isInput) {
                event.preventDefault();
                setIsActive((prev) => !prev);
                if (!isActive) {
                    setStatus('listening');
                }
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isActive]);

    const showRipples = status === 'listening' || status === 'speaking';

    return (
        <>
            <AnimatePresence>
                {isActive && (
                    <motion.div
                        initial={{ y: 100, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        exit={{ y: 100, opacity: 0 }}
                        transition={{ type: 'spring', damping: 20, stiffness: 300 }}
                        className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-4 pointer-events-none"
                    >
                        <motion.div
                            className="bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl p-6 flex flex-col items-center shadow-2xl"
                            initial={{ scale: 0.9 }}
                            animate={{ scale: 1 }}
                        >
                            <div className="relative w-32 h-32 flex items-center justify-center">
                                {showRipples && [1, 2, 3].map((ring) => (
                                    <motion.div
                                        key={ring}
                                        className={`absolute inset-0 rounded-full border ${
                                            status === 'speaking' ? 'border-green-500' : 'border-[var(--accent-primary)]'
                                        }`}
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: [0, 0.5, 0], scale: 1.5 }}
                                        transition={{
                                            duration: status === 'speaking' ? 0.5 : 2,
                                            repeat: Infinity,
                                            delay: ring * (status === 'speaking' ? 0.1 : 0.4),
                                            ease: 'easeOut',
                                        }}
                                    />
                                ))}

                                {status === 'processing' && (
                                    <motion.div
                                        className="absolute inset-0 rounded-full border-4 border-t-[var(--accent-primary)] border-r-transparent border-b-[var(--accent-primary)] border-l-transparent"
                                        animate={{ rotate: 360 }}
                                        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                                    />
                                )}

                                <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-[var(--accent-primary)] relative z-10 bg-black">
                                    <img
                                        src={computerIcon}
                                        alt="Voice Assistant"
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                            </div>

                            <div className="mt-4 flex flex-col items-center gap-1">
                                <span className="text-white font-medium text-lg tracking-wide">
                                    {statusText[status]}
                                </span>
                                {status === 'listening' && (
                                    <span className="text-white/50 text-xs uppercase tracking-wider">Speak Now</span>
                                )}
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {!isActive && (
                <div className="fixed bottom-4 left-1/2 -translate-x-1/2 text-xs text-white/30 pointer-events-none">
                    Press [Space] to talk
                </div>
            )}
        </>
    );
}
