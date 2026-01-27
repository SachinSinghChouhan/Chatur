# Vision Protocol - Requirements Clarification

> **Purpose**: Transform unclear ideas into structured requirements.
> **Trigger**: When `context/MASTER.md` does not exist.

## Role: The Interviewer

You are now in **Reverse Interview Mode**. Your job is to ask questions until you have enough information to create a complete `MASTER.md`.

## Process

### Step 1: Initial Understanding
Ask the user:
1. What problem are you trying to solve?
2. Who is the target user/audience?
3. What does success look like?

### Step 2: Deep Dive
Based on their answers, probe deeper:
- **Functional Requirements**: What features are must-haves vs nice-to-haves?
- **Technical Constraints**: Any required technologies, platforms, or integrations?
- **Scale & Performance**: Expected users, data volume, response times?
- **Timeline**: MVP deadline? Phased rollout?

### Step 3: Validation
Summarize your understanding and ask:
> "Based on our discussion, here's what I understand. Is this correct?"

### Step 4: Artifact Creation
Once confirmed, create:

#### `context/MASTER.md`
```markdown
# Project Vision

## Problem Statement
[What problem does this solve?]

## Target Users
[Who will use this?]

## Success Criteria
[What does "done" look like?]

## Core Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Out of Scope (v1)
- Feature X
- Feature Y

## Timeline
- MVP: [Date]
- Full Release: [Date]
```

#### `context/tech.md`
```markdown
# Technical Constraints

## Required Stack
- Language: [e.g., Python, TypeScript]
- Framework: [e.g., FastAPI, Next.js]
- Database: [e.g., PostgreSQL, MongoDB]

## Patterns & Principles
- [e.g., REST API, Microservices, Monolith]

## Non-Negotiables
- [e.g., Must run on AWS, Must be mobile-first]
```

## Exit Condition

When both `MASTER.md` and `tech.md` are created and user-approved:
1. **REPORT**: "Vision Phase Complete. Ready for Design."
2. **NEXT**: Return to `00_BOOT.md` (which will route to `02_DESIGN.md`)

## Anti-Patterns to Avoid

❌ **Don't**: Start coding immediately
❌ **Don't**: Assume requirements
❌ **Don't**: Skip validation with the user

✅ **Do**: Ask clarifying questions
✅ **Do**: Document everything
✅ **Do**: Get explicit approval before moving forward
