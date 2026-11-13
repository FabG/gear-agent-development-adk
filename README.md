# Develop Agents with Agent Development Kit (ADK)

This repository is a learning scaffold aligned to the Google Skills learning path: “Develop Agents with Agent Development Kit (ADK).” It is designed to mirror the course flow and hands-on lab progression for building, configuring, and extending AI agents with Google’s Agent Development Kit (ADK).

## Environment target

This repo is configured for learners using:

- macOS
- Python 3.11

The setup instructions are documented in [SETUP.md](SETUP.md).

## Purpose

The goal of this repo is to provide a practical study companion for the course and associated labs. It organizes the learning journey into clear stages:

- building a first agent
- configuring behavior and environment
- adding tools and integrations
- managing memory and state
- optimizing agent performance and decision quality
- connecting to external systems through MCP-based tools
- preparing for the skill badge and continued production work

## Learning path overview

The curriculum reflects the Google Skills path content, including:

1. Welcome: Develop Agents with Agent Development Kit (ADK)
2. Build Your First Agent with Agent Development Kit (ADK)
3. Add Agent Capabilities With Tools
4. Manage Agent Memory and State
5. Optimize Agent Behavior
6. Add Currency Tools to an Agent using MCP
7. Engineer AI Agents with Agent Development Kit (ADK) skill badge
8. Course wrap-up and next steps

This repo follows that order and provides folders for labs and exercises that support the same progression.

## Repository structure

```text
.
├── README.md
├── curriculum.md
├── courses/
│   ├── 01-welcome/
│   │   └── README.md
│   └── 02-build-your-first-agent/
│       └── README.md
├── labs/
│   ├── README.md
│   ├── 01-first-agent/
│   ├── 02-tools/
│   ├── 03-memory/
│   ├── 04-optimization/
│   ├── 05-mcp-tools/
│   └── 06-skill-badge/
└── .gitignore
```

## Suggested study flow

1. Read the course overview and objectives.
2. Complete the environment setup in the first lab.
3. Create a minimal ADK agent and run it locally.
4. Add tools and external capabilities.
5. Implement memory and session state for conversational continuity.
6. Improve agent behavior through instructions, model selection, and structured reasoning.
7. Connect tools through MCP to a real external service.
8. Complete the final skill-badge style practice and wrap-up review.

## Core concepts

### Quick reference

For a compact summary of the most important ADK settings, see [cheat-sheet-google-adk.md](cheat-sheet-google-adk.md).

### Agent Development Kit (ADK)
ADK provides a structured approach to building agent workflows, tool use, memory, orchestration, and deployment-ready logic.

### Tool calling
Agents become useful when they can connect to real capabilities such as web search, code execution, retrieval, and custom APIs.

### Memory and state
Stateful agents remember context, preferences, and prior interactions. This improves personalization and multi-turn conversation quality.

### Optimize Agent Behavior

The [Optimize Agent Behavior course](https://www.skills.google/paths/3545/course_templates/1564)
shows how to make agent behavior more predictable. Its structured-instructions
lessons explain why vague prompts lead to inconsistent scope, methods, tone, and
edge-case handling, then introduce five reusable patterns: **identity**,
**mission**, **methodology**, **boundaries**, and **few-shot examples**. The
course also covers structured output, model selection, and planning with ADK's
`BuiltInPlanner`.

The corresponding [optimization lab](labs/04-optimization/README.md) provides
a support-agent example and scenarios for applying the patterns and evaluating
their effect. It also explains [output tokens and sampling](labs/04-optimization/README.md#output-tokens-and-sampling)
to control response length and diversity with model-supported settings. The
[structured thinking section](labs/04-optimization/README.md#4-the-problem-complex-tasks-need-structured-thinking)
introduces `BuiltInPlanner`, thinking configuration, planner selection, and a
hands-on problem-solving exercise. [Section 5](labs/04-optimization/README.md#5-putting-it-all-together-agent-patterns)
combines these skills into seven agent examples, also collected with code in the
[cheat sheet](cheat-sheet-google-adk.md#agent-examples). [Section 6](labs/04-optimization/README.md#6-common-pitfalls-to-avoid)
reviews common instruction, configuration, planning, and output pitfalls. Start
with the lesson on [structured instructions](https://www.skills.google/paths/3545/course_templates/1564/html_bundles/686132).

### MCP
The Model Context Protocol (MCP) makes it possible for agents to interact with external tools and services in a standardized, extensible way.

## Lab progression

Each lab folder contains exercises and implementation prompts that map to the course flow.

- [labs/01-first-agent](labs/01-first-agent/README.md) – set up and run a simple ADK agent
- [labs/02-tools](labs/02-tools/README.md) – attach external tools to the agent
- [labs/03-memory](labs/03-memory/README.md) – manage session state and memory
- [labs/04-optimization](labs/04-optimization/README.md) – tune prompts, planning, and model behavior
- [labs/05-mcp-tools](labs/05-mcp-tools/README.md) – connect to a tool server using MCP
- [labs/06-skill-badge](labs/06-skill-badge/README.md) – final capstone and review tasks

## Getting started

1. Clone the repository.
2. Open the course modules in order.
3. Follow the lab instructions in each folder.
4. Use the final project as a reference implementation and portfolio artifact.

## License

This repository is intended as a learning and training companion for the Google Skills ADK path. Use it for study, experimentation, and portfolio development.

## Notes

This repo is a curated educational scaffold based on the public Google Skills path. It is meant to help learners organize the course material and practical lab work in a single place.
