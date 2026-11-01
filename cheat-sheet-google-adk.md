# Google ADK Cheat Sheet

This quick reference summarizes the core concepts you use when building a first agent with Google Agent Development Kit (ADK).

## The four core parameters

Every basic ADK agent is defined by four important parameters:

### 1. `model`
Choose the LLM that powers the agent.

- Example: `gemini-2.0-flash`
- This tells the agent which model to use for reasoning and response generation.
- The model is the "brain" of the agent.

### 2. `name`
Give the agent a clear identifier.

- Example: `root_agent`
- This is the label used inside the agent system and helps keep the project organized.
- Use a simple, descriptive name.

### 3. `description`
Describe what the agent does.

- Example: `A helpful assistant for user questions.`
- This helps explain the role and purpose of the agent.
- Keep it short and specific.
- **description vs. instruction:** While peer agents read `description` externally to decide task routing, the agent itself reads `instruction` internally to guide its tone, rules, and actions.

### 4. `instruction`
Define the behavior and constraints of the agent.

- Example: `Answer user questions to the best of your knowledge.`
- This is the main guidance the model follows.
- It controls the persona, tone, scope, and expectations.

## The root_agent naming convention

In ADK, the main agent is commonly named `root_agent` because it is the top-level agent that coordinates everything else.

This naming convention is helpful because:

- it makes the entry point obvious in code
- it clearly signals that this is the main orchestration object
- it matches the default pattern used in starter projects

Example:

```python
root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

Use `root_agent` when you are creating the primary agent for a simple project. Later, as your project grows, you may add more specialized agents and give them names that reflect their responsibilities.

### Can the internal name be different from the variable name?

Yes. The variable name in Python can be different from the agent’s internal `name` value.

For example, this is valid:

```python
assistant_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

Here:

- variable name: `assistant_agent`
- internal agent name: `root_agent`

This is useful when you want a clearer Python variable name while preserving the conventional ADK identity name.

## Minimal example

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

## Remember this pattern

An ADK agent is not just a model call. It is the combination of:

- model
- tools
- orchestration

The four parameters above are the foundation for the agent’s identity and behavior.

## Quick tips

- Use a clear `name` so your project stays readable.
- Keep the `description` short and role-based.
- Write `instruction` as clear operational guidance.
- Start simple; you can add tools and memory later.

## Related references

- [README.md](README.md)
- [courses/02-build-your-first-agent/README.md](courses/02-build-your-first-agent/README.md)
- [labs/01-first-agent/README.md](labs/01-first-agent/README.md)
