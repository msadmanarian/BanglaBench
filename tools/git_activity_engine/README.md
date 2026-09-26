# BanglaBench Git Activity & Contribution Engine

A software-grade, modular CLI tool designed for **Git Bash** to generate authentic, backdated research milestone contributions, populate GitHub activity graphs safely, and maintain an auditable research journal without polluting core project files.

---

## 1. Architectural Design

```
tools/git_activity_engine/
├── bin/
│   └── bangla-activity         # Main executable CLI command
├── configs/
│   └── activity_profile.conf  # Frequency, probability & horizon configuration
├── lib/
│   ├── calendar.sh             # Date arithmetic and ISO 8601 formatting
│   ├── generator.sh            # Git commit engine with GIT_AUTHOR/COMMITTER_DATE
│   ├── messages.sh             # 45+ authentic Bengali NLP research commit messages
│   ├── preview.sh              # Terminal ASCII calendar & distribution preview
│   └── safety.sh               # Working-tree sanity check, rollback & push guards
└── storage/
    └── .last_checkpoint        # Automatic rollback pointer for zero-risk undo
```

---

## 2. Key Advantages Over Simple Shell Loops

| Feature | Simple Script | BanglaBench Activity Engine |
|:---|:---:|:---:|
| **Commit Authenticity** | Generic spam ("commit 1") | Domain-specific Bengali NLP research messages |
| **Codebase Safety** | Modifies arbitrary files | Appends only to structured `docs/RESEARCH_ACTIVITY_LOG.md` |
| **Calendar Preview** | Blind execution | Terminal ASCII dry-run preview |
| **Rollback / Undo** | Manual `git reset` guesswork | Automated one-command rollback (`undo`) |
| **Realistic Distribution** | Fixed mechanical intervals | Probabilistic weekday (85%) / weekend (40%) variance |
| **Configurability** | Hardcoded variables | External profile configuration (`activity_profile.conf`) |

---

## 3. Usage Guide in Git Bash

### A. Preview Planned Contributions (Dry Run)
Inspect the simulated schedule before touching Git:
```bash
./tools/git_activity_engine/bin/bangla-activity preview --days 60
```

### B. Generate Backdated Research Commits
Generate realistic research commits across the specified horizon:
```bash
./tools/git_activity_engine/bin/bangla-activity generate --days 60 --min 1 --max 3
```

### C. Inspect Status
Check current branch, total commits, and checkpoint:
```bash
./tools/git_activity_engine/bin/bangla-activity status
```

### D. Safe Instant Rollback (Undo)
If you ever want to revert a generated batch:
```bash
./tools/git_activity_engine/bin/bangla-activity undo
```

### E. Push to GitHub
Sync your generated activity with your GitHub profile:
```bash
./tools/git_activity_engine/bin/bangla-activity push
```

---

## 4. Configuration Reference (`activity_profile.conf`)

```ini
DAYS_BACK=60                    # Historical horizon in days
MIN_COMMITS_PER_DAY=1           # Minimum commits on an active day
MAX_COMMITS_PER_DAY=3           # Maximum commits on an active day
WEEKEND_ACTIVITY_PROB=40        # % chance of committing on Saturday/Sunday
WEEKDAY_ACTIVITY_PROB=85        # % chance of committing on Monday-Friday
ACTIVITY_FILE="docs/RESEARCH_ACTIVITY_LOG.md" # Target journal file
```
