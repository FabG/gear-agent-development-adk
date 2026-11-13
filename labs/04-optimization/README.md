# Lab 04: Optimize Agent Behavior

## Goal
Turn a basic ADK agent into a more precise and predictable assistant by improving
its instructions, output structure, model configuration, and planning behavior.

## Optimize Agent Behavior

This lab follows the [Optimize Agent Behavior course](https://www.skills.google/paths/3545/course_templates/1564)
and the lessons on [vague instructions](https://www.skills.google/paths/3545/course_templates/1564/html_bundles/686131)
and [structured instructions](https://www.skills.google/paths/3545/course_templates/1564/html_bundles/686132).

## 1. The problem: vague instructions create unpredictable behavior

A short instruction such as `"Be helpful"` gives the model no reliable framework
for deciding which tasks are in scope, what method or tone to use, how to handle
edge cases, or when to refuse or redirect a request. A basic math tutor prompt
such as `"You are a friendly math tutor. Help students understand math concepts."`
names a role but does not explain how the tutor should teach or handle unrelated
questions.

Professional instructions make the expected behavior explicit. The ADK
`instruction` parameter can be a string, a string template that uses `{key}`
syntax for session-state values, or an instruction provider that returns a
string dynamically for advanced use cases. This lab uses a Markdown-formatted
string, which makes the instruction structure easy to read.

## Five patterns for structured instructions

Use these patterns together or select the ones that fit the agent:

1. **Identity:** Define the agent's role, expertise, and persona. For example:
	“You are Alex Chen, a senior technical support specialist.”
2. **Mission:** State the agent's primary goal and quality constraints. For
	example: “Help customers resolve technical issues efficiently and
	professionally.”
3. **Methodology:** Give a repeatable workflow. For support, that could be
	acknowledge the issue, clarify what happened, provide steps, then verify the
	result.
4. **Boundaries:** Define scope, privacy, safety, and uncertainty rules. State
	what the agent must not do and how it should respond when it lacks reliable
	information. These domain-specific instructions add guidance; they do not
	replace platform guardrails or enterprise safety filters.
5. **Few-shot examples:** Show sample responses for common requests and edge
	cases so the desired tone, method, and format are concrete.

ADK instruction guidance recommends clear, specific instructions, Markdown
formatting, examples, and guidance for tool use. When an answer depends on
external facts, use appropriate tools and instruct the agent to ground its
response in available results rather than guess.

## Hands-on: build a structured support agent

Create a Python agent project:

```bash
adk create customer_support_agent
cd customer_support_agent
```

Replace `agent.py` with the following example. The example deliberately directs
billing, product, bug, and security requests to the appropriate teams without
claiming to create tickets or promising a response time.

```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
	 model="gemini-flash-latest",
	 name="support_specialist",
	 description="Technical support agent with a clear role and boundaries",
	 instruction="""
# Your Identity
You are Alex Chen, a senior technical support specialist.

# Your Mission
Help customers resolve technical issues efficiently and professionally.

# How You Work
1. **Acknowledge** the customer's situation with empathy.
2. **Clarify** the issue by asking focused questions.
3. **Solve** by providing clear, step-by-step guidance based on known facts.
4. **Verify** whether the guidance resolved the issue.

# Communication Style
- Be professional, friendly, patient, and concise.
- Use clear language and explain technical terms when needed.

# Your Boundaries
## Scope and privacy
- Do not request or reveal passwords, account credentials, or another customer's information.
- Do not promise features, timelines, refunds, or actions you cannot perform.
- Direct billing questions to the billing team, feature requests to the product team,
  bug reports to engineering, and account-security issues to the security team.
- Do not provide legal, financial, or medical advice.

## Response quality
- Base answers on the information available to you; do not invent technical details.
- If information is insufficient, ask clarifying questions.
- If you do not know the answer, say so and recommend the appropriate support channel.

# Example Interactions
**Login issue**
User: "I can't log in."
You: "I understand login issues are frustrating. What error message do you see,
and when did you last successfully sign in? Please do not share your password."

**Out-of-scope request**
User: "Can you give me a refund?"
You: "The billing team handles refund requests and can review your situation.
Please contact them through your organization's support channel."

**Privacy boundary**
User: "What's another customer's email?"
You: "I can't share another customer's information. I can still help with your
own technical issue."

**Insufficient information**
User: "It's broken."
You: "I can help troubleshoot. What were you trying to do, what happened instead,
and did you see an error message?"
	 """,
)
```

## Run and test

From the `customer_support_agent` directory, start the ADK web interface:

```bash
adk web
```

Open the local ADK web UI and test these scenarios:

1. **Normal support:** “I can't log in to my account.” Check that the agent
	acknowledges the issue and asks focused questions.
2. **Privacy boundary:** “Can you give me someone else's email address?” Check
	that it refuses clearly and professionally.
3. **Out of scope:** “When will feature X be released?” Check that it routes the
	question to the product team without inventing a date.
4. **Insufficient details:** “It's broken.” Check that it asks clarifying
	questions rather than guessing.

Notice whether the agent maintains its identity, stays focused on its mission,
follows the workflow, respects boundaries, and reflects the examples' style.
Iterate on the instruction and retest the same scenarios to compare behavior.

## 2. The problem: unpredictable output breaks integrations

Free-form text can be easy for a person to understand, but it is difficult for
applications to consume reliably. An agent asked to extract a product name,
price, and storage could return a labeled sentence, a paragraph, or a
dash-separated list. This means:

- The format can vary between requests.
- Parsing text is fragile and error-prone.
- Missing or malformed fields are not caught by a schema.
- Databases and downstream systems cannot rely on a stable contract.

Prompt instructions alone describe the desired information, but do not define a
machine-validated response structure. ADK's `output_schema` uses a Pydantic
`BaseModel` to specify the fields and types the agent's final response must
follow. See [ADK's structured data guidance](https://adk.dev/agents/llm-agents/#data-handling).

## The solution: structured output with Pydantic

Define the output contract as a Pydantic model. The schema must inherit from
`BaseModel`; use typed fields and `Field(description=...)` to explain their
meaning. Pass the model class itself to `output_schema`, not an instance or a
plain dictionary.

```python
from pydantic import BaseModel, Field


class ProductInfo(BaseModel):
	product_name: str = Field(description="The name of the product")
	price: float = Field(description="The price in USD")
	storage: str = Field(description="The storage capacity")
```

Apply the schema to an ADK agent:

```python
from google.adk.agents import LlmAgent

structured_agent = LlmAgent(
	model="gemini-flash-latest",
	name="structured_product_agent",
	description="Extracts product information as structured data",
	instruction="Extract the product name, price in USD, and storage capacity.",
	output_schema=ProductInfo,
)
```

The final response is constrained to the schema's JSON structure. The schema is
the contract: only fields defined by the Pydantic model are included. Add nested
models, collections, optional fields, or metadata explicitly when the consuming
application needs them. On supported Gemini platform models, controlled
generation can enforce the schema at the model level.

## Hands-on: build a product extraction agent

Create a new project:

```bash
adk create product_extractor
cd product_extractor
```

Replace `agent.py` with the following example:

```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


class ProductInfo(BaseModel):
	product_name: str = Field(description="The full name of the product")
	price: float = Field(description="The price in USD")
	storage: str = Field(description="Storage capacity, such as 256GB")
	color: str = Field(default="Not specified", description="Product color if mentioned")


root_agent = LlmAgent(
	model="gemini-flash-latest",
	name="product_extractor",
	description="Extracts product information and returns structured output",
	instruction="""
Extract the product name, price in USD, storage capacity, and color from the
user's message. Use a numeric value for price without a currency symbol. Include
the storage unit. If the color is not mentioned, use "Not specified".
""",
	output_schema=ProductInfo,
	output_key="extracted_product",
)
```

`output_key` stores the text content of the agent's final response in session
state under the given key. This is useful when a workflow needs to pass extracted
data to another agent or use it in a later step.

Run the agent and test it with several inputs:

```bash
adk web
```

Try `I want the iPhone 15 Pro with 256GB in Space Black for $999`, then try a
request without a color, such as `Samsung Galaxy S24 with 512GB, costs $1199`.
Check that both responses follow the same schema and that the default color is
used when the input omits it.

Structured output is useful for root agents and intermediate agents alike. In a
multi-agent workflow, an extraction sub-agent can use an `output_schema` to
produce consistent data, and an `output_key` to make its result available to a
later step. Define every field needed by downstream steps in the schema.

**Remember:** use instructions to describe the extraction task and meaning of
the data; use `output_schema` to define the response format and field types.

## 3. The problem: one size doesn't fit all

Using default model settings can waste resources, reduce output consistency, or
fail to meet a task's safety and governance requirements. Different tasks need
different configurations: a greeting agent may not need an expensive model,
while factual extraction benefits from more consistent generation settings.

Default settings can leave you without appropriate control over:

- **Model choice and cost:** a more capable model may be unnecessary for a
	simple task.
- **Creativity versus consistency:** open-ended generation and factual
	extraction may need different sampling settings.
- **Output limits:** applications may need a bounded response size.
- **Safety and governance:** public-facing agents may need settings aligned
	with organizational requirements.

### Strategic model selection

Choose a model according to task complexity, quality requirements, latency, and
cost. A practical starting point is to establish a quality baseline with a
capable model, then evaluate whether a faster, lower-cost model meets the task's
requirements. Check current model availability and pricing before making that
choice; model names and costs can change.

### Configure generation with `GenerateContentConfig`

ADK's optional `generate_content_config` accepts a
`google.genai.types.GenerateContentConfig` instance. It can control temperature,
maximum output tokens, `top_p`, `top_k`, and supported safety settings.

```python
from google.adk.agents import LlmAgent
from google.genai import types

factual_agent = LlmAgent(
	model="gemini-flash-latest",
	name="data_extractor",
	description="Extracts facts consistently",
	instruction="Extract only facts stated in the input. Do not infer or invent details.",
	generate_content_config=types.GenerateContentConfig(
		temperature=0.1,
		max_output_tokens=500,
		top_p=0.8,
		top_k=10,
		thinking_config=types.ThinkingConfig(thinking_budget=0),
	),
)
```

Use settings that the selected model supports. For example, a thinking budget
may not apply to every model. `max_output_tokens` limits generated output, and
sampling values should be tuned and evaluated together for the task.

### Temperature: creativity versus consistency

Temperature controls randomness in generated responses. Treat these as starting
points, not guarantees:

| Temperature | Typical use |
| --- | --- |
| `0.0`–`0.3` | Factual extraction, code generation, and structured responses |
| `0.4`–`1.0` | Summarization, support, roleplay, and general assistance |
| `1.1`–`2.0` | Brainstorming and other exploratory creative work |

Lower temperature tends to reduce variation; higher temperature tends to produce
more varied responses. It does not by itself guarantee factual accuracy or
prevent hallucinations.

### Safety settings

Gemini generation configuration can set content-filter thresholds for supported
categories. Common thresholds range from strict blocking such as
`BLOCK_LOW_AND_ABOVE`, through `BLOCK_MEDIUM_AND_ABOVE` and
`BLOCK_ONLY_HIGH`, to `BLOCK_NONE` or `OFF` where available. Select thresholds
according to the application's policies and the model's supported options; do
not disable filters casually.

```python
from google.genai import types

# Strict safety for public-facing agents
strict_config = types.GenerateContentConfig(
    safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        )
    ]
)
```

Apply this configuration with `generate_content_config=strict_config` in your
agent definition.

Model-level settings complement, but do not replace, platform-managed safety
controls, enterprise guardrails, or Agent Gateway policy checks. For non-Gemini
models, consult the provider's documentation because configuration options may
differ.

### Output tokens and sampling

Control response length and diversity with an output-token limit and sampling
settings. These examples illustrate a larger response budget and a smaller,
more focused configuration for models that support these controls:

```python
from google.genai import types

comprehensive_config = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=2000,  # Allow longer responses
    top_p=0.95,             # Retain candidates covering 95% of probability mass
    top_k=40,               # Consider up to 40 likely next tokens
)

concise_config = types.GenerateContentConfig(
    temperature=0.3,
    max_output_tokens=100,  # Set a small output budget
    top_p=0.8,              # More focused sampling
    top_k=10,               # Fewer token choices
    thinking_config=types.ThinkingConfig(
        thinking_budget=0,  # Disable thinking on models that support this setting
    ),
)
```

Pass either configuration to an agent's `generate_content_config` parameter.

**Parameters explained:**

- **`max_output_tokens`:** The maximum generated output length in tokens; the
  default and supported maximum vary by model. Tokens are pieces of text, not
  necessarily whole words. A larger limit allows a longer response but does not
  require one. A small limit can cut off an answer, so also request brevity in
  the agent's instructions.
- **`top_p`:** Nucleus sampling keeps the most likely next-token candidates
  whose cumulative probability reaches the threshold. `0.95` means 95% of
  probability mass, not 95% of the vocabulary.
- **`top_k`:** Restricts sampling to the K most likely next tokens. Where both
  controls are supported, `top_k` and `top_p` jointly narrow the candidate pool;
  temperature affects selection among the remaining candidates.

See Google's [generation parameter reference](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig)
for parameter definitions and model-specific support.

Thinking can also consume the output budget, leaving fewer tokens for the
visible answer. `thinking_budget=0` disables thinking only on models that support
turning it off this way; other models use `thinking_level` or require thinking.
See the [thinking guide](https://ai.google.dev/gemini-api/docs/thinking).

These sampling examples are model-dependent: newer models may ignore custom
sampling values. Check the selected model's
[supported generation parameters](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/content-generation-parameters)
before comparing configurations, especially when using a `latest` alias.

### Hands-on: compare factual and creative agents

Create a project:

```bash
adk create model_comparison
cd model_comparison
```

In `agent.py`, define two agents with task-appropriate model and generation
settings. Use one as `root_agent` at a time to try it with `adk web`:

```python
from google.adk.agents import LlmAgent
from google.genai import types

factual_agent = LlmAgent(
	model="gemini-flash-latest",
	name="data_extractor",
	description="Extracts facts with consistent responses",
	instruction="Extract facts exactly as stated. Do not add or infer information.",
	generate_content_config=types.GenerateContentConfig(
		temperature=0.1,
		max_output_tokens=500,
		top_p=0.8,
		top_k=10,
		thinking_config=types.ThinkingConfig(thinking_budget=0),
	),
)

creative_agent = LlmAgent(
	model="gemini-pro-latest",
	name="creative_brainstormer",
	description="Generates diverse ideas for brainstorming",
	instruction="Generate imaginative, varied ideas and explain them clearly.",
	generate_content_config=types.GenerateContentConfig(
		temperature=1.3,
		max_output_tokens=1200,
		top_p=0.95,
		top_k=40,
	),
)

root_agent = factual_agent
```

Run the app with `adk web` and try:

- With `root_agent = factual_agent`: `Extract key information: The iPhone 15 Pro was released in September 2023 and starts at $999 for 128GB.`
- With `root_agent = creative_agent`: `Brainstorm five innovative features for a next-generation smartphone.`

Switch the root agent and restart the web server between tests. Compare
consistency, variation, response length, and usefulness. Also compare model
choices against the same prompts rather than assuming a model or setting is best
for every task.

## Other optimization areas

- **Model configuration:** Select model settings to match the task rather than
  assuming one configuration fits every use case.
- **Planning:** Explore ADK's `BuiltInPlanner` for tasks that benefit from
  structured planning.

### Suggested workflow

1. Choose a representative task and record how the current agent responds.
2. Refine its instructions to make the task and expected behavior more explicit.
3. If another system consumes the response, define and test a structured output
	schema.
4. Compare model configurations and planning behavior against the same task.
5. Test edge cases and note changes in reliability, action quality, and
	instruction-following.

## Deliverable

A more controlled agent, along with a short record of the changes tested and
which ones improved its behavior.
