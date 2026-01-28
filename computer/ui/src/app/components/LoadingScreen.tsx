import React, { useEffect, useState } from 'react';
import { motion } from 'motion/react';

export const LoadingScreen = ({ onComplete }: { onComplete: () => void }) => {
    useEffect(() => {
        // Wait for a few seconds to simulate initialization, then trigger completion
        const timer = setTimeout(() => {
            onComplete();
        }, 2800); // 2.8 seconds total duration

        return () => clearTimeout(timer);
    }, [onComplete]);

    // Animation variants for the sound wave bars
    const waveVariants = {
        initial: {
            height: 10,
            opacity: 0.3,
        },
        animate: (i: number) => ({
            height: [10, 35, 10, 25, 10],
            opacity: [0.3, 1, 0.3, 0.8, 0.3],
            transition: {
                repeat: Infinity,
                duration: 1.2,
                ease: "easeInOut" as const, // Fix type inference
                delay: i * 0.15, // Stagger effect
            },
        }),
    };

    return (
        <motion.div
            className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#0F1115]"
            initial={{ opacity: 1 }}
            exit={{ opacity: 0, transition: { duration: 0.8, ease: "easeInOut" } }}
        >
            {/* Sound Wave Container */}
            <div className="flex items-center justify-center gap-1.5 h-16 mb-6">
                {[0, 1, 2, 3, 4].map((i) => (
                    <motion.div
                        key={i}
                        custom={i}
                        variants={waveVariants}
                        initial="initial"
                        animate="animate"
                        className="w-1.5 rounded-full bg-slate-500/80"
                    />
                ))}
            </div>

            {/* Text Container */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5, duration: 1 }}
                className="text-center"
            >
                <p className="text-sm font-medium tracking-widest text-[#71717A] uppercase opacity-80">
                    Initializing voice assistant...
                </p>
            </motion.div>
        </motion.div>
    );
};
