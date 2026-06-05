# OpenHire

## Setup Guide

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: venv\Scripts\activate
pip install pip-tools
pip-sync requirements.txt
```

## How to Install New Package

This project uses [pip-tools](https://pip-tools.readthedocs.io/) to manage dependencies.

- `requirements.in` — direct dependencies only; **edit this file**
- `requirements.txt` — fully pinned lockfile; **generated, never edit manually**

**1. Add the package to `requirements.in`:**
```
celery
```

**2. Recompile the lockfile:**
```bash
pip-compile requirements.in
```

**3. Sync your virtual environment:**
```bash
pip-sync requirements.txt
```
