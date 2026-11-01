# Course 2: Build Your First Agent with Agent Development Kit (ADK)

This course is the hands-on implementation step in the Google Skills ADK learning path. It moves learners from concept to practice by guiding them through the setup of a local ADK environment and the creation of a working AI agent that can respond to user prompts.

## Course overview

This course continues from the first lab and the earlier welcome module. The goal is to move from understanding the agent concept to creating your first working ADK project.

In this course, learners convert the ideas from the welcome module into a live agent implementation. The focus is practical: configure the environment, define the agent, run it locally, and confirm that it behaves as expected.

The main theme is simple: build a first working agent before layering on tools, memory, optimization, and external integrations.

### Related lab

- [Lab 1: Build Your First Agent](../../labs/01-first-agent/README.md)

### Reference content

- [Set up: Build Your First Agent](https://www.skills.google/paths/3545/course_templates/1563/html_bundles/687397)
- [Define agent identity: Build Your First Agent](https://www.skills.google/paths/3545/course_templates/1563/html_bundles/687399)

## Learning objectives

By the end of this course, learners should be able to:

- set up a development environment for Agent Development Kit (ADK)
- create a basic agent configuration and understand its key parameters
- run the agent in a local or interactive environment
- test the agent with realistic prompts and evaluate its output
- recognize the core structure required for more advanced ADK workflows

## Why this course matters

The first agent is the foundation for every later stage of the path. If the environment is set up correctly and the basic agent works, the next tasks—tools, memory, optimization, and MCP integrations—become much easier to reason about and implement.

A successful first agent is not just a demo. It is the baseline from which you extend behavior, add capabilities, and improve reliability.

## Core concepts introduced

### 1. Agent environment setup
Learners prepare the local workspace with the dependencies, configuration, and runtime requirements needed to build and execute ADK agents.

This includes:
- creating or opening a project folder
- installing runtime dependencies
- configuring model access or environment variables
- making sure the project can run locally

### 2. Agent definition
A basic agent typically includes:
- a name and identity
- a system prompt or instruction set
- model configuration
- execution behavior for receiving and responding to events or prompts

This phase focuses on how these parts work together in a simple, understandable design.

### 3. Running the agent
After the agent is created, learners test it by sending sample prompts, checking output quality, and verifying the architecture works end-to-end.

### 4. Observing behavior
The learner begins evaluating real agent behavior, including:
- clarity of response
- prompt adherence
- structure of outputs
- known limitations or areas for tuning

## Suggested lesson flow

### Lesson 1: Set up the environment
Topics:
- install dependencies
- prepare project files
- confirm runtime is working
- identify required environment variables and API configuration
- scaffold the project with `adk create my_first_agent`

This step corresponds to the setup flow in the Google Skills course material.

### Lesson 2: Define your first agent
Topics:
- explain agent structure
- create the system prompt
- choose a model or configuration
- define simple interaction behavior
- set the agent `name`, `description`, and `instruction`

A basic ADK agent definition often looks like this:

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

This is the identity layer of the agent: it tells the model who it is, what it should do, and how it should behave.

### Lesson 3: Run and test the agent
Topics:
- execute the agent locally
- send sample prompts
- capture outputs and review quality
- confirm the environment is stable before moving to advanced features

## Practical lab guidance

### Lab objective
Build a simple ADK agent that can answer a user question and run successfully in a local development environment.

### Minimum deliverables
- working local project or workspace
- a basic agent file or configuration
- sample prompts and observed outputs
- notes on what worked and what could be improved

### Recommended prompts for testing
- "What is an AI agent?"
- "Summarize how an agent differs from a chatbot."
- "Help me plan a small project for building an ADK agent."
- "Give me a concise explanation of how agent development works."

### Success criteria
The learner has successfully created a working agent if:

- the project starts without errors
- the agent responds to prompts
- outputs are coherent and relevant
- the learner understands the structure of the agent enough to extend it later

## Exercise ideas

### Exercise 1: Build the baseline
Create a minimal agent with a simple system prompt and a few example interactions.

### Exercise 2: Compare behavior
Test the same request with different wording or prompt structures and note how the answer changes.

### Exercise 3: Document the design
Write a short architecture note explaining:
- what the agent does
- what its prompt is
- what parts of the setup are important for future work

## Common pitfalls to avoid

- skipping environment setup and assuming the agent will run immediately
- making the prompt too vague or too broad
- testing only one input instead of multiple scenarios
- not documenting observations for later optimization steps

## Expected outcomes

After completing this course, learners should be comfortable with the basic ADK workflow and ready to add capabilities that make agents more useful in real scenarios.

The next step is to extend the agent with tools and external actions, which is covered in the next course of the learning path.

## Next step

Continue to the next course in the path: Add Agent Capabilities With Tools.
