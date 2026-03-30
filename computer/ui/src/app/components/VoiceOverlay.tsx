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

// ─── Waveform ────────────────────────────────────────────────────────────────

const BAR_COUNT = 24;

// Stable per-bar params — deterministic so they never change between renders
const BAR_PARAMS = Array.from({ length: BAR_COUNT }, (_, i) => ({
    duration: 0.30 + (i % 6) * 0.07,          // 0.30 – 0.65 s cycle
    delay:    (i * 0.045) % 0.38,              // 0 – 0.38 s stagger
    maxH:     10 + ((i * 7 + 3) % 3) * 10,    // 10 | 20 | 30 px
}));

function WaveformBars({ status }: { status: Status }) {
    const active = status !== 'processing';

    // listening → accent blue-slate, speaking → green, processing → flat gray
    const color =
        status === 'speaking'
            ? '#22c55e'
            : status === 'listening'
            ? 'var(--accent-secondary)'
            : 'rgba(255,255,255,0.15)';

    return (
        <div className="flex items-end justify-center gap-[2.5px] h-9 w-52">
            {BAR_PARAMS.map((bar, i) => (
                <motion.div
                    key={i}
                    style={{
                        backgroundColor: color,
                        width: 3,
                        borderRadius: 2,
                        minHeight: 3,
                    }}
                    animate={
                        active
                            ? { height: [3, bar.maxH, 3] }
                            : { height: 3 }
                    }
                    transition={
                        active
                            ? {
                                  duration: bar.duration,
                                  delay:    bar.delay,
                                  repeat:   Infinity,
                                  ease:     'easeInOut',
                              }
                            : { duration: 0.25 }
                    }
                />
            ))}
        </div>
    );
}

// ─── Main overlay ─────────────────────────────────────────────────────────────

export function VoiceOverlay() {
    const [isActive, setIsActive] = useState(false);
    const [status, setStatus]     = useState<Status>('listening');

    // WebSocket — auto-reconnects
    useEffect(() => {
        let ws: WebSocket | null = null;
        let reconnectTimer: number | undefined;

        const connect = () => {
            try {
                ws = new WebSocket(WS_URL);

                ws.onopen = () => console.log('[Chatur] overlay connected');

                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        const next = data?.status as string;

                        if (next === 'idle' || next === 'state_change' && data?.state === 'idle') {
                            window.setTimeout(() => setIsActive(false), HIDE_DELAY_MS);
                        } else if (next === 'listening' || data?.state === 'listening') {
                            setIsActive(true);
                            setStatus('listening');
                        } else if (next === 'processing' || data?.state === 'processing') {
                            setIsActive(true);
                            setStatus('processing');
                        } else if (next === 'speaking' || data?.state === 'speaking') {
                            setIsActive(true);
                            setStatus('speaking');
                        }
                    } catch (e) {
                        console.error('[Chatur] WS parse error', e);
                    }
                };

                ws.onclose = () => {
                    reconnectTimer = window.setTimeout(connect, RECONNECT_DELAY_MS);
                };

                ws.onerror = () => ws?.close();
            } catch (e) {
                console.error('[Chatur] connection error', e);
            }
        };

        connect();
        return () => {
            ws?.close();
            if (reconnectTimer) window.clearTimeout(reconnectTimer);
        };
    }, []);

    // Space key toggle (for testing in browser)
    useEffect(() => {
        const onKey = (e: KeyboardEvent) => {
            const isInput = e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement;
            if (e.code === 'Space' && !e.repeat && !isInput) {
                e.preventDefault();
                setIsActive((prev) => !prev);
                if (!isActive) setStatus('listening');
            }
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, [isActive]);

    const showRipples = status === 'listening' || status === 'speaking';

    return (
        <>
            <AnimatePresence>
                {isActive && (
                    <motion.div
                        initial={{ y: 100, opacity: 0 }}
                        animate={{ y: 0,   opacity: 1 }}
                        exit={{   y: 100,  opacity: 0 }}
                        transition={{ type: 'spring', damping: 20, stiffness: 300 }}
                        className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 flex flex-col items-center gap-4 pointer-events-none"
                    >
                        <motion.div
                            className="bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl px-8 py-6 flex flex-col items-center shadow-2xl gap-5"
                            initial={{ scale: 0.9 }}
                            animate={{ scale: 1 }}
                        >
                            {/* ── Icon + ripples ── */}
                            <div className="relative w-28 h-28 flex items-center justify-center">
                                {showRipples && [1, 2, 3].map((ring) => (
                                    <motion.div
                                        key={ring}
                                        className={`absolute inset-0 rounded-full border ${
                                            status === 'speaking'
                                                ? 'border-green-500'
                                                : 'border-[var(--accent-secondary)]'
                                        }`}
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: [0, 0.4, 0], scale: 1.6 }}
                                        transition={{
                                            duration: status === 'speaking' ? 0.55 : 2,
                                            repeat:   Infinity,
                                            delay:    ring * (status === 'speaking' ? 0.12 : 0.45),
                                            ease:     'easeOut',
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

                                <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-[var(--accent-primary)] relative z-10 bg-black">
                                    <img
                                        src={computerIcon}
                                        alt="Voice Assistant"
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                            </div>

                            {/* ── Waveform ── */}
                            <WaveformBars status={status} />

                            {/* ── Label ── */}
                            <div className="flex flex-col items-center gap-1 -mt-1">
                                <motion.span
                                    key={status}
                                    initial={{ opacity: 0, y: 4 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`font-medium text-base tracking-wide ${
                                        status === 'speaking'
                                            ? 'text-green-400'
                                            : status === 'processing'
                                            ? 'text-white/70'
                                            : 'text-white'
                                    }`}
                                >
                                    {statusText[status]}
                                </motion.span>

                                {status === 'listening' && (
                                    <span className="text-white/40 text-[10px] uppercase tracking-widest">
                                        Speak Now
                                    </span>
                                )}
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {!isActive && (
                <div className="fixed bottom-4 left-1/2 -translate-x-1/2 text-[11px] text-white/25 pointer-events-none tracking-widest uppercase">
                    Press [Space] to talk
                </div>
            )}
        </>
    );
}
