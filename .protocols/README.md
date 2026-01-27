# Protocol System

> An Operating System for AI Agents to deliver professional-grade software.

## What is This?

The Protocol System is a structured framework that guides AI agents through the complete software development lifecycle (SDLC). It prevents "LLM confusion" by enforcing a disciplined approach: **Vision → Design → Implementation → Delivery**.

## Philosophy

**Constraints = Clarity**

By forcing the AI to follow strict protocols, we ensure:
- ✅ Requirements are clear before coding starts
- ✅ Architecture is designed before implementation
- ✅ Code follows professional standards
- ✅ Deliverables are production-ready

## Quick Start

### For AI Agents

1. **Boot**: Read `.protocols/00_BOOT.md` at the start of every session
2. **Follow**: The boot kernel will route you to the correct protocol
3. **Execute**: Complete the protocol's requirements before moving forward

### For Humans

1. **Initialize**: Create a new project by having the AI read `00_BOOT.md`
2. **Collaborate**: Answer the AI's questions during the Vision phase
3. **Review**: Approve design documents before implementation begins
4. **Deploy**: Use the generated deployment artifacts

## Directory Structure

```
.protocols/
├── 00_BOOT.md          # Entry point - routes to correct phase
├── 01_VISION.md        # Requirements gathering protocol
├── 02_DESIGN.md        # Architecture design protocol
├── 03_IMPLEMENT.md     # Implementation protocol (TDD)
├── 04_DELIVER.md       # Production delivery protocol
└── context/            # Project memory
    ├── MASTER.md       # Project vision & goals
    ├── tech.md         # Tech stack & constraints
    ├── design/         # Architecture artifacts
    │   ├── architecture.md
    │   ├── api_spec.md
    │   └── file_structure.md
    └── active/         # Current work
        └── TASK.md     # Active task details
```

## The Four Phases

### 1. Vision (01_VISION.md)
**Goal**: Transform vague ideas into clear requirements.

**Process**: Reverse interview mode where the AI asks questions until it can create:
- `context/MASTER.md` - Project vision and requirements
- `context/tech.md` - Technical constraints

### 2. Design (02_DESIGN.md)
**Goal**: Create comprehensive technical design before coding.

**Rule**: 🛑 NO CODE ALLOWED until design is approved.

**Artifacts**:
- `context/design/architecture.md` - System architecture
- `context/design/api_spec.md` - API contracts
- `context/design/file_structure.md` - Project structure

### 3. Implementation (03_IMPLEMENT.md)
**Goal**: Build the system following TDD principles.

**Process**: Plan → Test → Code → Verify → Document

**Quality Standards**:
- Tests required
- Error handling mandatory
- Documentation inline
- Design spec compliance

### 4. Delivery (04_DELIVER.md)
**Goal**: Make the system production-ready.

**Artifacts**:
- `Dockerfile` & `docker-compose.yml`
- CI/CD pipeline (`.github/workflows/`)
- Complete documentation (`README.md`, `DEPLOYMENT.md`)
- Environment configuration

## Key Features

### State-Based Routing
The boot kernel automatically determines which phase you're in and routes accordingly.

### Context Persistence
All project knowledge is stored in `context/` for session continuity.

### Quality Enforcement
Each protocol has built-in quality standards and anti-patterns to avoid.

### Professional Standards
Every deliverable meets production-ready criteria.

## Example Workflow

```bash
# Session 1: Vision
AI reads 00_BOOT.md → No MASTER.md exists → Routes to 01_VISION.md
AI interviews user → Creates MASTER.md and tech.md

# Session 2: Design
AI reads 00_BOOT.md → MASTER.md exists, no design/ → Routes to 02_DESIGN.md
AI creates architecture, API spec, file structure → User approves

# Session 3-N: Implementation
AI reads 00_BOOT.md → TASK.md exists → Routes to 03_IMPLEMENT.md
AI implements features following TDD → Marks tasks complete

# Final Session: Delivery
User commands "deliver" → AI follows 04_DELIVER.md
AI creates Docker, CI/CD, docs → System is production-ready
```

## Inspiration

This system was inspired by:
- **UCP (Unified Context Protocol)**: The concept of a "boot kernel" for AI agents
- **Traditional SDLC**: Waterfall's discipline + Agile's iteration
- **The Vision**: From the original audio transcript emphasizing "constraints reduce confusion"

## License

MIT - Use this however you want. Attribution appreciated but not required.
