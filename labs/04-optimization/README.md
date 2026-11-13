# Lab 04: Optimize Agent Behavior

## Goal
Turn a basic ADK agent into a more precise and predictable assistant by improving
its instructions, output structure, model configuration, and planning behavior.

## Optimize Agent Behavior

This lab follows the [Optimize Agent Behavior course](https://www.skills.google/paths/3545/course_templates/1564)
and the lessons on [vague instructions](https://www.skills.google/paths/3545/course_templates/1564/html_bundles/686131)
and [structured instructions](https://www.skills.google/paths/3545/course_templates/1564/html_bundles/686132).

## The problem: vague instructions create unpredictable behavior

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

## The problem: unpredictable output breaks integrations

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
