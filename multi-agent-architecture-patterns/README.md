# Multi-Agent Architecture Patterns

Six multi-agent patterns, each run as a hands-on lab against the DAS
(Data Archival System) chatbot used throughout this training. Standalone
project: it only depends on this folder's own `archive.py` and `data/`.


## Setup

Copy `.env.example` to `.env` and fill in Nexus's URL and key:

```
NEXUS_BASE_URL=https://nexus.example.internal/v1
NEXUS_API_KEY=...
NEXUS_MODEL=MODEL-NAME
```

Every lab reads these from the environment — nothing is hardcoded.

## Run

```
uv run <FileName>
```

Each lab prints one trace line per agent step, so the pattern's flow is
visible while it runs.
