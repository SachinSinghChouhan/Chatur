# Project Vision: Computer - Personal PC Voice Assistant

## Problem Statement

Current voice assistants (Alexa, Google Assistant) are either mobile-focused or cloud-dependent, requiring users to open apps manually. There's a need for a desktop-native voice assistant that:
- Runs seamlessly in the background on Windows PCs
- Activates via wake word without manual app launching
- Provides personal, always-available assistance for daily tasks
- Maintains privacy with local processing where possible

## Target Users

**Primary (v1):** Personal use by the project creator
**Secondary (future):** Technical and non-technical Windows users seeking a privacy-conscious, desktop-integrated voice assistant

## Success Criteria

### MVP Success (v1)
- ✅ User can activate assistant hands-free using wake word "Computer"
- ✅ Assistant reliably responds to voice commands in English
- ✅ Reminders trigger at correct times with voice + toast notifications
- ✅ Timers work accurately
- ✅ Simple notes/facts persist across PC restarts
- ✅ Runs as background service from Windows startup

### Long-term Success
- Natural bilingual support (English + Hindi/Hinglish)
- Advanced conversational memory
- System automation capabilities
- Message sending integration

## Core Requirements (v1)

### Must-Have Features
- [x] Wake word detection ("Hi Computer", "Sun Computer")
- [x] Voice command recognition (English + Hindi/Hinglish)
- [x] Question answering (general knowledge, help)
- [x] Reminder system (date/time based)
- [x] Timer functionality
- [x] Simple memory store (notes, key-value facts)
- [x] Background service (auto-start with Windows)
- [x] System tray interface (mic toggle, status, exit)
- [x] Voice + Windows toast notifications
- [x] App launching (Chrome, Gmail, Calculator, etc.)
- [x] Spotify control (Play/Pause/Next/Previous)

### Technical Requirements
- [x] Windows-only support
- [x] Offline wake word detection
- [x] Hybrid cloud/local architecture
- [x] Persistent local storage (survives restarts)
- [x] Low resource footprint

## Out of Scope (v1)

- ❌ Mac/Linux support
- ❌ WhatsApp message sending
- ❌ Email sending (Gmail/Outlook)
- ❌ Advanced system automation
- ❌ Complex conversational context memory
- ❌ Recurring reminders
- ❌ Multi-user support
- ❌ Mobile companion app

## Timeline

- **MVP Deadline:** Saturday/Sunday (January 25-26, 2026)
- **Current Date:** Tuesday, January 21, 2026
- **Available Time:** ~4-5 days

## Project Phases

1. **Vision** (Current) - Requirements clarification ✓
2. **Design** - Architecture & system design
3. **Implementation** - Core development
4. **Delivery** - Testing, polish, deployment

## Wake Word Configuration

**Name:** Computer  
**Activation Phrases:**
- "Hi Computer"
- "Sun Computer"

## Notification Strategy

**Reminders:**
- Voice alert (Text-to-Speech)
- Windows toast notification
- Both triggered simultaneously

**Timers:**
- Voice alert on completion
- Toast notification
