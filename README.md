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

### Agent Development Kit (ADK)
ADK provides a structured approach to building agent workflows, tool use, memory, orchestration, and deployment-ready logic.

### Tool calling
Agents become useful when they can connect to real capabilities such as web search, code execution, retrieval, and custom APIs.

### Memory and state
Stateful agents remember context, preferences, and prior interactions. This improves personalization and multi-turn conversation quality.

### Optimization
Agent behavior can be improved through better prompts, model selection, planning strategies, and clear operational constraints.

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
