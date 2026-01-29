// Overlay-only entry point
import React from 'react';
import { createRoot } from 'react-dom/client';
import { VoiceOverlay } from './app/components/VoiceOverlay';
import './index.css';

// Render just the overlay
createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <VoiceOverlay />
    </React.StrictMode>
);
