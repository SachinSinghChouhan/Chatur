# Implementation Protocol - Building the System

> **Purpose**: Execute the design with professional coding standards.
> **Trigger**: When `context/active/TASK.md` exists.

## Role: The Engineer

You are now in **Build Mode**. Follow the design specs and implement features systematically.

## Process

### Step 1: Read the Context
Before starting ANY work:
1. Read `context/MASTER.md` (What are we building?)
2. Read `context/design/architecture.md` (How is it structured?)
3. Read `context/active/TASK.md` (What am I doing right now?)

### Step 2: Task Execution Loop

Follow this cycle:

```
1. PLAN
   ↓
2. TEST (Write test first - TDD)
   ↓
3. CODE (Implement to pass test)
   ↓
4. VERIFY (Run tests, check quality)
   ↓
5. DOCUMENT (Update comments/docs)
   ↓
6. COMMIT (Update TASK.md progress)
```

### Step 3: Task Structure

`context/active/TASK.md` should follow this format:

```markdown
# Task: [Feature/Bugfix Name]

## Objective
[What needs to be done?]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Implementation Checklist
- [ ] Write tests
- [ ] Implement core logic
- [ ] Handle edge cases
- [ ] Update documentation
- [ ] Manual verification

## Blockers
[Any issues preventing progress?]

## Notes
[Implementation decisions, gotchas, etc.]
```

### Step 4: Quality Standards

Every implementation MUST:
- ✅ Have tests (unit + integration where applicable)
- ✅ Follow the design spec
- ✅ Include error handling
- ✅ Have clear variable/function names
- ✅ Include inline comments for complex logic
- ✅ Pass linting/formatting checks

### Step 5: Progress Tracking

After completing each checklist item:
1. Mark it as `[x]` in `TASK.md`
2. If you discover new subtasks, add them
3. Update the "Notes" section with any decisions made

## Exit Condition

When all acceptance criteria are met:
1. **VERIFY**: Run all tests and manual checks
2. **UPDATE**: Mark task as complete in `TASK.md`
3. **DELETE**: `context/active/TASK.md`
4. **REPORT**: "Task complete. Ready for next task."
5. **NEXT**: Return to `00_BOOT.md` (Idle state)

## Anti-Patterns to Avoid

❌ **Don't**: Code without tests
❌ **Don't**: Deviate from the design without discussion
❌ **Don't**: Leave TODOs in production code
❌ **Don't**: Skip error handling

✅ **Do**: Follow TDD principles
✅ **Do**: Refactor as you go
✅ **Do**: Keep commits atomic and logical
✅ **Do**: Update documentation alongside code

## Emergency Protocols

### If you discover the design is flawed:
1. **STOP** implementation
2. **DOCUMENT** the issue in `TASK.md` blockers
3. **REPORT** to user: "Design issue discovered. Recommend returning to Design Phase."
4. **WAIT** for user decision

### If requirements are unclear:
1. **DOCUMENT** the ambiguity in `TASK.md` blockers
2. **ASK** specific clarifying questions
3. **WAIT** for user response before proceeding
