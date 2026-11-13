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

## Agent examples

These examples combine instruction writing, model configuration, structured
output, and planning. Each snippet is independent; choose one as a starting
point and adapt it to your domain.

The model aliases, sampling settings, and numeric thinking budgets below follow
the preceding lessons. Verify support for the selected model: some models use
`thinking_level`, ignore sampling overrides, or cannot disable thinking.
`include_thoughts=True` requests available summaries, not raw internal reasoning.
Low temperature does not guarantee deterministic or policy-compliant output.

The schemas retain flexible dictionaries from the course examples. For a stable
integration, prefer explicitly typed nested models and check the backend's
supported JSON Schema subset. Validate returned JSON and business rules before
using the result. See [Gemini structured output guidance](https://ai.google.dev/gemini-api/docs/structured-output).

`output_key` stores the final response text in **session state**. A key named
`approval_review` is not a Boolean approval, and setting it does not automatically
write to Memory Bank. Persistent sessions and long-term memory require their
own services and configuration. See [ADK session state](https://adk.dev/sessions/state/).

For the full learning context, see [optimization section 5](labs/04-optimization/README.md#5-putting-it-all-together-agent-patterns).
Export the selected agent as `root_agent` to load it with ADK; for example,
`root_agent = customer_agent`.

### Customer intake and ticket classification

Combines structured ticket output with native thinking. It drafts ticket details; creating a ticket requires a separate tool or integration.

```python
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from pydantic import BaseModel, Field
from typing import Dict, Any

class TicketOutput(BaseModel):
    ticket: Dict[str, Any] = Field(description="Ticket details")
    priority: str = Field(description="Priority level")

customer_agent = LlmAgent(
    model="gemini-flash-latest",
    name="customer_service_agent",
    description="Handles customer intake, classification, and ticketing",
    instruction="""You are a customer intake specialist. Summarize the issue and
classify its priority using the supplied policy. Ask for missing details.
Do not request credentials or claim that a ticket has been created.""",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=1024)
    ),
    output_schema=TicketOutput
)
```

### Dataset analysis

Returns insights and metrics from supplied data. Use calculation tools for reliable numerical analysis when needed.

```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AnalysisOutput(BaseModel):
    insights: List[str] = Field(description="Key insights")
    metrics: Dict[str, Any] = Field(description="Performance metrics")

analysis_agent = LlmAgent(
    model="gemini-pro-latest",
    name="data_processing_agent",
    description="Analyzes input datasets and produces structured metric outputs",
    instruction="""Analyze only the supplied dataset. Identify trends and report
metrics with their units and assumptions. Flag missing data; do not invent it.""",
    output_schema=AnalysisOutput
)
```

### Approval-routing workflow

Combines process instructions, generation settings, and a session-state output key. It recommends routing without executing approval actions.

```python
from google.adk.agents import LlmAgent
from google.genai import types

workflow_agent = LlmAgent(
    model="gemini-flash-latest",
    name="approval_workflow_agent",
    description="Drafts policy checks and approval-routing recommendations",
    instruction="""Compare the request with the policy supplied by the user.
Identify the applicable rules and recommend an approval route. If policy or
evidence is missing, request it. Do not claim to grant approval or execute actions.""",
    output_key="approval_review",
    generate_content_config=types.GenerateContentConfig(
         temperature=0.1,  # Lower variation where supported
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            )
        ]
    )
)
```

### Educational tutor

Combines a teaching methodology with planning, without requesting thought summaries.

```python
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

tutor_agent = LlmAgent(
    model="gemini-pro-latest",
    name="educational_tutor_agent",
    description="Provides guided step-by-step tutoring using deliberate pedagogical planning",
    instruction="""Act as a patient tutor. Assess the learner's understanding,
ask one guiding question at a time, and give hints before a solution.
Explain mistakes respectfully and check understanding.""",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=2048)
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=4000,
    ),
)
```

### Reusable professional service template

Combines instructions, planning, structured output, and generation settings. Replace every bracketed placeholder before use.

```python
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from pydantic import BaseModel, Field
from typing import Dict, Any

class ServiceResponse(BaseModel):
    response: str = Field(description="The response to the user")
    action_required: bool = Field(description="Whether action is needed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

professional_agent = LlmAgent(
    model="gemini-flash-latest",
    name="service_pro",
    description="Professional service agent handling customer requests with structured output",
    instruction="""
    # PERSONA
    You are [Name], a [Role] with [Experience].

    # BOUNDARIES
    Never: [List of restrictions]
    Always: [List of requirements]

    # EXAMPLES
    [Few-shot examples]
    """,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=1024)
    ),
    output_schema=ServiceResponse,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2500,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            )
        ]
    )
)
```

### Structured entity extraction

Extracts typed entities and relationships. Confidence scores are model estimates, not calibrated probabilities.

```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from google.genai import types

class Entity(BaseModel):
    type: str = Field(description="Entity type")
    value: str = Field(description="Entity value")
    confidence: float = Field(ge=0, le=1, description="Uncalibrated model confidence, 0-1")

class ExtractionOutput(BaseModel):
    entities: List[Entity] = Field(description="Extracted entities")
    relationships: List[str] = Field(description="Relationships found")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extraction metadata")

extractor = LlmAgent(
    model="gemini-flash-latest",
    name="data_extractor",
    description="Extracts structured entities and relationships from raw text",
    instruction="Extract structured data from text",
    output_schema=ExtractionOutput,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Lower variation where supported
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,  # Only where disabling thinking is supported
        ),
        max_output_tokens=1000,
    ),
)
```

### Policy decision support

Uses planning to assess a request and stores the recommendation in session state for downstream review.

```python
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

decision_agent = LlmAgent(
    model="gemini-pro-latest",
    name="decision_maker",
    description="Evaluates requests against organizational policies",
    instruction="""
    Evaluate requests against the supplied organizational policy.
    Cite applicable rules and identify missing evidence or dependencies.
    Return a recommendation for review; do not grant approval or execute actions.
    """,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=2048)
    ),
    output_key="approval_review",  # Store result in session state
    generate_content_config=types.GenerateContentConfig(
         temperature=0.1,  # Lower variation where supported
        max_output_tokens=3000,
    ),
)
```

## Quick reference card

### Model selection strategy

```text
1. Establish a quality baseline: Gemini Pro is a useful candidate for complex tasks.
2. Compare Gemini Flash: Evaluate production throughput, latency, quality, and cost.
3. Perform gap analysis when switching Pro → Flash using the same tasks and metrics.
```

This is a comparison strategy, not a requirement to start every project with Pro.
Choose the model that meets the measured requirements.

### Temperature guide

```text
0.0–0.3: Facts, data extraction, code generation, lower variation
0.4–1.0: Balanced chat, general assistance, customer support
1.1–2.0: Experiments with creative writing, divergent brainstorming, marketing copy
```

These are starting points for models supporting this temperature range, not
guarantees of accuracy or creativity. Some models ignore sampling overrides;
follow the selected model's guidance and evaluate results.

### Safety thresholds

```text
BLOCK_LOW_AND_ABOVE: Blocks low, medium, and high probability ratings
BLOCK_MEDIUM_AND_ABOVE: Blocks medium and high probability ratings
BLOCK_ONLY_HIGH: Blocks high probability ratings
BLOCK_NONE: Does not block based on the configured category's probability threshold
OFF: Disables the configurable filter where supported; behavior depends on backend
```

`BLOCK_LOW_AND_ABOVE` is the strictest of these probability thresholds. Select
settings for the audience and use case, then test legitimate and unsuitable
requests. Public-facing or child-facing use needs more than a threshold choice.
`BLOCK_NONE` and `OFF` do not imply unrestricted generation or removal of all
platform safeguards. Availability and rating behavior depend on the backend;
see [Gemini safety settings](https://ai.google.dev/gemini-api/docs/safety-settings).

### When to use what

```text
BuiltInPlanner: Compatible thinking-capable Gemini models, multi-step tasks, dependencies
PlanReActPlanner: Explicit plan-and-act structure, including models without native thinking
output_schema: Pydantic BaseModel defining structured JSON output in these examples
output_key: Store final response text in session state for later steps or agents
```

`PlanReActPlanner` is not limited to non-Gemini models. `output_key` does not
extract a field automatically: parse and validate structured response text when
a downstream step needs a particular value.

### Instruction patterns

```text
Identity: [Name], [Role], [Expertise]
Mission: What the agent does
Methodology: How the agent works
Boundaries: Never/Always lists
Few-shot: Input → Output examples
```

## Related references

- [README.md](README.md)
- [courses/02-build-your-first-agent/README.md](courses/02-build-your-first-agent/README.md)
- [labs/01-first-agent/README.md](labs/01-first-agent/README.md)
