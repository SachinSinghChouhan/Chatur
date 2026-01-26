# Background Service & System Tray - Quick Reference

## Running the Assistant

### Console Mode (Text Input)
```bash
python -m chatur.main
# OR
python run_console.py
```

### System Tray Mode (Background)
```bash
python run_tray.py
```

## System Tray Menu

Right-click the tray icon to access:

- **Status** - Check if running/stopped/error
- **Start/Stop** - Control the assistant
- **Restart** - Restart the service
- **Open Logs** - View log file
- **About** - Version info
- **Exit** - Shutdown

## Icon States

- 🟢 **Green Microphone** - Assistant is running
- ⚫ **Gray Microphone** - Assistant is stopped
- 🔴 **Red Microphone** - Error occurred

## Testing

```bash
# Test service manager
python test_service_manager.py

# Test console mode
python run_console.py

# Test tray mode
python run_tray.py
```

## Files Created

- `chatur/service/service_manager.py` - Service lifecycle management
- `chatur/ui/system_tray.py` - System tray interface
- `chatur/ui/icons/` - Tray icons (active/inactive/error)
- `run_tray.py` - Tray mode launcher
- `run_console.py` - Console mode launcher

## Next Steps

1. Test both modes
2. Fix voice input (Azure STT or Whisper)
3. Add wake word detection
4. Package as executable

## Troubleshooting

**Tray icon not showing:**
- Check system tray hidden icons (click ^)
- Verify `pystray` is installed
- Check `chatur/ui/icons/` exists

**Service won't start:**
- Check `logs/chatur.log`
- Try console mode first
- Verify database initialized

**Can't stop service:**
- Use Exit from tray menu
- Wait 5 seconds for graceful shutdown
- Check Task Manager if frozen
