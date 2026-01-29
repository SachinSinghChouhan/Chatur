# How to Use ChaturAssistant.exe

## Quick Start Guide

### Step 1: Launch the Application
Double-click `ChaturAssistant.exe` in:
```
d:\protocol\computer\dist\ChaturAssistant.exe
```

You should see:
- ✅ System tray icon appears (bottom-right of Windows taskbar)
- ✅ No console window (runs silently in background)

### Step 2: Open the Voice Overlay Interface
The voice assistant has a **web-based overlay**. You need to open it in your browser:

1. Open any web browser (Chrome, Edge, Firefox)
2. Navigate to: **http://localhost:8000**
3. You should see the voice assistant interface

### Step 3: Activate with Ctrl+Space
Once the web page is open:

1. Press **Ctrl+Space**
2. Overlay appears at bottom-center showing "Listening..."
3. Speak your command
4. Watch the overlay transition:
   - "Listening..." → "Thinking..." → "Speaking..." → Hidden

## Tray Icon Menu

Right-click the tray icon to see:
- **Voice Assistant** - Shows current status
- **Press Ctrl+Space to activate** (informational)
- **About** - Version info
- **Exit** - Closes the application

## Important Notes

⚠️ **The overlay ONLY works when you have http://localhost:8000 open in your browser**

The executable runs TWO components:
1. **Backend Server** (runs in background on port 8000)
2. **Web UI** (must be accessed via browser)

## Alternative: Keep Browser Open
For best experience:
- Keep a browser tab open at `localhost:8000`
- Minimize the browser window
- Press Ctrl+Space anytime to activate
- The overlay will appear on top of all windows

## Troubleshooting

### "Page can't be reached"
- Wait 5-10 seconds after launching the exe
- Check if port 8000 is already in use
- Check logs: `%APPDATA%\Computer\logs\computer.log`

### Ctrl+Space doesn't work
- Make sure browser tab is open to `localhost:8000`
- Check that no other app is using Ctrl+Space
- Try pressing Space key in the browser (fallback test)

### No audio response
- Check Azure Speech credentials in `.env` file
- Verify microphone permissions
- Check speaker volume
