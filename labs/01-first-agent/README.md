# Lab 01: Build Your First Agent

## Goal
Create a minimal but working Agent Development Kit (ADK) agent on macOS using Python 3.11. This lab is the foundation for everything that follows in the learning path.

## Environment

- Operating system: macOS
- Python: 3.11
- Terminal: bash/zsh
- Recommended virtual environment: `.venv`

## Learning objectives

By the end of this lab, you should be able to:

- prepare a Python 3.11 environment for ADK work
- install the required dependencies
- create a minimal agent definition with instructions and model settings
- run the agent locally
- test the agent against a few prompt examples
- document the output quality and identify next improvements

## Prerequisites

Before starting the lab, make sure you have:

- macOS installed and running locally
- Python 3.11 available in your shell
- Git installed
- access to a Google AI / Gemini model configuration or API setup supported by your ADK environment

## Step 1: Create a virtual environment

From the repo root, create and activate a local environment:

```bash
cd /path/to/gear-agent-development-adk
python3.11 -m venv .venv
source .venv/bin/activate
python --version
```

You should see Python 3.11.x.

## Step 2: Install dependencies

Install the package(s) required for ADK development. The exact package name can vary depending on the ADK version, but the pattern is typically:

```bash
python -m pip install --upgrade pip
python -m pip install google-adk
```

Verify the installation immediately after a successful install:

```bash
adk --version
```

If your ADK setup requires additional dependencies, install them as needed alongside the core package.

## Get your API Key

Your agent needs access to a large language model or LLM (the “Model” component from course 1). For this course, we’ll use Google’s Gemini models.

1. Visit [Google AI Studio](https://aistudio.google.com/apikey).
2. Sign in with your Google account.
3. Click **Create API Key.**
4. Copy the API key (it looks like **AIzaSyC**...).

If your environment uses a different authentication mechanism (for example, Google AI Studio or Vertex AI), configure the required environment variables before running the agent.

Examples:

```bash
export GOOGLE_API_KEY="your-api-key"
```

or whatever your ADK setup requires.

## Step 3: Create your first agent project

ADK provides a command to scaffold a new agent project with the correct structure.

```bash
adk create my_first_agent
```

What this creates:

```text
my_first_agent/
├── agent.py      # Main agent code (you’ll edit this)
├── __init__.py   # Python package initialization
└── .env          # Environment variables (you’ll edit this next)
```

After the project is created, open the generated folder and review the files before making any custom changes.

## Step 4: Create a basic agent file

Create a file such as `agent.py`:

```python
from __future__ import annotations

# Adapt the import style to the exact ADK version you installed.
# The goal is to define a minimal agent with instructions and a model.

# Example skeleton:
# from google.adk import Agent


def build_agent():
    """Return a minimal agent definition for this lab."""
    # Replace this with the actual ADK client/agent API used by your environment.
    return {
        "name": "first_agent",
        "model": "gemini-2.0-flash",
        "instruction": (
            "You are a helpful assistant. "
            "Answer clearly, briefly, and with practical examples when helpful."
        ),
    }


if __name__ == "__main__":
    agent = build_agent()
    print(f"Agent created: {agent['name']}")
    print(f"Model: {agent['model']}")
    print(f"Instruction: {agent['instruction']}")
```

This is intentionally simple. The important idea is that a working ADK agent should have:

- a name
- a model configuration
- a clear instruction set
- a way to receive user input and produce a response

## Step 5. Verify your set up

Let’s confirm everything works by running the ADK web interface.

### Start the ADK web interface:

```bash
adk web
```

### Expected output:

```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### What this does

- Starts a local web server at http://localhost:8000/
- Opens a browser tab automatically
- Provides a visual interface to interact with your agent

### Success indicators:

- No error messages seen in the terminal
- Browser opens to the ADK interface.
- You see the web UI with your agent name.

## Alternative way to run the agent


```bash
adk run .
```


## Step 6: Test with realistic prompts

Use a few sample prompts to check that the agent responds correctly.

Suggested prompts:

```text
What is an AI agent?

Explain the difference between a chatbot and an agent.

Help me plan a simple Python project for a personal assistant.

Give me a short summary of how ADK agents are built.
```

Record the outputs and check for:

- clarity
- relevance
- consistency
- prompt adherence
- whether the text is structured and useful

## Step 8: Understanding your setup

Let’s connect what you just built to the concepts from Course 1.

### The three components in your environment

Remember: Agent = model + tools + orchestration.

#### Model:
- The framework that runs the agent loop
- Manages: Perceive → think → act → check → repeat
- You installed this in step 4 (pip install google-adk)

#### Tools:
*(Coming in the Other ways to run your agent module)*

- Functions your agent can call to take actions.
- Examples: search the web, read files, and send emails.
- These bridge “knowing” to “doing”.

#### Orchestration (from ADK):
- The framework that runs the agent loop
- Manages: Perceive → think → act → check → repeat
- You installed this in step 4 (pip install google-adk)

## Step 9: Review and refine

This lab is intentionally simple, but it is where you learn the base pattern for all future work.

Ask yourself:

- Does the agent answer clearly?
- Is the instruction prompt specific enough?
- Did the agent follow the expected scope?
- What would make it more useful in a real application?

## Deliverable

A working minimal agent project that includes:

- Python 3.11 environment setup
- required dependency installation
- a simple agent definition
- at least one successful run
- sample prompt outputs documented in notes

## Suggested lab notes

Create a short lab log with:

- environment details
- installed dependencies
- agent definition summary
- example prompts and responses
- what worked and what should change next

## Common pitfalls

- using the wrong Python version
- forgetting to activate the virtual environment
- missing environment variables for the model connection
- designing a prompt that is too vague or too broad
- assuming the first version is final

## Success criteria

Your lab is successful when:

- the environment works on macOS with Python 3.11
- the agent starts without errors
- the agent responds to user input
- you can explain the basic structure of how the agent is built

## Next step

The next lab builds on this by adding tools and real capabilities to the agent.
