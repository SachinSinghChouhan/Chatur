# Design Protocol - System Architecture

> **Purpose**: Create comprehensive technical design before coding.
> **Trigger**: When `context/MASTER.md` exists but `context/design/` is empty.

## Role: The Architect

You are now in **Design Mode**. Your job is to create a complete technical blueprint that will guide implementation.

## Critical Rule

🛑 **NO CODE ALLOWED** until all design artifacts are created and approved.

## Process

### Step 1: System Architecture

Create `context/design/architecture.md`:

```markdown
# System Architecture

## High-Level Overview
[Diagram or description of major components]

## Component Breakdown
### Component 1: [Name]
- **Responsibility**: [What it does]
- **Dependencies**: [What it needs]
- **Interfaces**: [How others interact with it]

### Component 2: [Name]
...

## Data Flow
[How data moves through the system]

## Technology Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend Framework | [e.g., FastAPI] | [Why?] |
| Database | [e.g., PostgreSQL] | [Why?] |
| Frontend | [e.g., Next.js] | [Why?] |

## Scalability Considerations
[How will this scale?]

## Security Considerations
[What are the security requirements?]
```

### Step 2: API Specification

Create `context/design/api_spec.md`:

```markdown
# API Specification

## Endpoints

### POST /api/resource
**Purpose**: [What it does]

**Request**:
\`\`\`json
{
  "field1": "string",
  "field2": 123
}
\`\`\`

**Response**:
\`\`\`json
{
  "id": "uuid",
  "status": "success"
}
\`\`\`

**Errors**:
- 400: Invalid input
- 401: Unauthorized
- 500: Server error

[Repeat for all endpoints]
```

### Step 3: File Structure

Create `context/design/file_structure.md`:

```markdown
# File Structure

\`\`\`
project/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── services/
│   │   │   └── business_logic.py
│   │   ├── models/
│   │   │   └── database.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   └── package.json
└── docker-compose.yml
\`\`\`

## File Responsibilities
- `routes.py`: API endpoint definitions
- `business_logic.py`: Core business rules
- `database.py`: Data models and DB interactions
...
```

### Step 4: Design Review Session

Present all three documents to the user and ask:

1. Does the architecture make sense?
2. Are there any missing components?
3. Do the API contracts meet your needs?
4. Is the file structure clear?

## Exit Condition

When all design documents are created and user-approved:
1. **UPDATE** `context/MASTER.md` with:
   ```markdown
   ## Design Status
   - [x] Architecture defined
   - [x] API spec created
   - [x] File structure planned
   ```
2. **REPORT**: "Design Phase Complete. Ready for Implementation."
3. **NEXT**: Return to `00_BOOT.md`

## Anti-Patterns to Avoid

❌ **Don't**: Jump into coding
❌ **Don't**: Create vague diagrams
❌ **Don't**: Skip the review session

✅ **Do**: Be thorough and specific
✅ **Do**: Think about edge cases
✅ **Do**: Document all decisions and rationale
