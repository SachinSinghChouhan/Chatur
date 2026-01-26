# Computer Voice Assistant - Manual Testing Guide

## Quick Test Instructions

Run the main application and test each feature manually:

```bash
python -m chatur.main
```

---

## Test Checklist

### ✅ Test 1: Timers

**Commands to try:**
```
Start a timer for 10 seconds
Set a timer for 2 minutes
Timer for 30 seconds
```

**Expected:**
- ✅ Confirms timer started
- ✅ Shows duration
- ✅ Timer completes and shows notification

---

### ✅ Test 2: Reminders

**Commands to try:**
```
Set a reminder for 5 PM
Remind me to call mom tomorrow at 9 AM
Reminder for 2 minutes from now
```

**Expected:**
- ✅ Confirms reminder created
- ✅ Shows scheduled time
- ✅ Reminder triggers at scheduled time (check after waiting)

---

### ✅ Test 3: Notes/Memory

**Commands to try:**
```
Remember my favorite color is blue
Remember my birthday is January 15
Save that my car is a Honda
```

**Then retrieve:**
```
What's my favorite color?
When is my birthday?
What car do I have?
```

**Expected:**
- ✅ Confirms note saved
- ✅ Retrieves correct information

---

### ✅ Test 4: Questions

**Commands to try:**
```
What's the capital of France?
Who invented the telephone?
What is 25 times 4?
```

**Expected:**
- ✅ Provides accurate answers
- ✅ Responds in natural language

---

### ✅ Test 5: App Launching

**Commands to try:**
```
Open Chrome
Open Calculator
Launch Notepad
Open Gmail
```

**Expected:**
- ✅ Confirms app launching
- ✅ App actually opens

---

### ✅ Test 6: Media Control

**Prerequisites:** Spotify must be running

**Commands to try:**
```
Play music
Pause music
Next song
Previous track
```

**Expected:**
- ✅ Spotify responds to commands
- ✅ Playback changes

---

### ✅ Test 7: Bilingual (Hindi/Hinglish)

**Commands to try:**
```
5 minute ka timer lagao
Kal subah 8 baje reminder set karo
Chrome kholo
```

**Expected:**
- ✅ Understands Hindi/Hinglish
- ✅ Responds appropriately

---

## Quick Automated Test

If you want to run automated tests without manual input:

```bash
# Test all handlers quickly
python test_computer.py

# Test reminder scheduler
python test_scheduler.py
```

---

## Results Tracking

Mark each test as you complete it:

- [ ] Timers work
- [ ] Reminders work
- [ ] Notes work
- [ ] Questions work
- [ ] App launching works
- [ ] Media control works
- [ ] Bilingual support works
- [ ] Scheduler triggers reminders automatically

---

## Common Issues

**Timer doesn't complete:**
- Wait the full duration
- Check console for "Timer complete" message

**Reminder doesn't trigger:**
- Scheduler checks every 30 seconds
- Wait up to 30 seconds after scheduled time

**App doesn't launch:**
- Check if app is installed
- Try with Calculator (always available on Windows)

**Media control doesn't work:**
- Make sure Spotify is running
- Try play/pause first

---

## Next Steps After Testing

Once all tests pass:
1. Document any issues found
2. Decide on next feature priority:
   - Background service
   - System tray
   - Wake word detection
