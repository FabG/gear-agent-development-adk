# Local Setup for Mac OS + Python 3.11

This repository is designed for learners working on macOS with Python 3.11 as the target runtime for the ADK labs.

## Prerequisites

- macOS
- Python 3.11 installed
- Git
- a terminal with shell access

## Verify Python version

```bash
python3 --version
```

Expected result:

```bash
Python 3.11.x
```

If you have multiple Python versions available, explicitly use:

```bash
python3.11 --version
```

## Recommended Python management

If Python 3.11 is not already installed, use `pyenv`:

```bash
brew install pyenv
pyenv install 3.11.9
pyenv local 3.11.9
```

Then verify:

```bash
python3 --version
```

## Create a virtual environment

From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

You should see Python 3.11.x.

## Upgrade pip

```bash
python -m pip install --upgrade pip
```

## Install project dependencies

Install the package dependencies required by the course or lab environment:

```bash
pip install -r requirements.txt
```

If the repo does not yet include a `requirements.txt`, create one later as the specific lab exercises require it.

## Notes for the labs

- Use `python3.11` when creating the environment.
- Prefer `source .venv/bin/activate` for each terminal session.
- Keep the Python runtime stable across labs so experiments are consistent.
- Treat each lab as a separate mini-project inside the repo if needed.

## Recommended workflow

```bash
cd /path/to/gear-agent-development-adk
python3.11 -m venv .venv
source .venv/bin/activate
python --version
pip install --upgrade pip
pip install -r requirements.txt
```

This setup matches the local lab environment for this repository and keeps the course exercises consistent with your Mac + Python 3.11 configuration.
