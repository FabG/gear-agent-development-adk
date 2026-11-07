# Challenge Lab: Engineer AI Agents with ADK

**Source:** [Google Skills challenge lab](https://www.skills.google/paths/3545/course_templates/1596/labs/647534)

## Challenge scenario

You have joined Cymbal Travel, a travel agency that uses AI agents to find travel updates, validate destination data, and audit brochure claims. The prototypes for its Travel Scout and Brochure Auditor are misconfigured or incomplete: the Scout has no Google Search tool, and the Auditor's multi-agent pipeline is missing its Reviser stage.

Your task is to repair and run the agents so downstream systems receive accurate, consistent travel information.

## Project contents

The downloaded `adk_project` directory contains:

- `my_google_search_agent`: the Travel Scout, which must search for current events.
- `geo_validator`: the Destination Verifier, which must return a structured capital-city result.
- `llm_auditor`: the Brochure Auditor, a sequential critic-and-reviser pipeline.

## Task 1: Install ADK and set up the environment

In the Google Cloud Skills lab, open Cloud Shell and install ADK:

```bash
export PATH="$PATH:/home/${USER}/.local/bin"
python3 -m pip install google-adk
```

Authenticate to Google Cloud and configure Application Default Credentials:

```bash
gcloud auth application-default login
```

Follow the sign-in flow shown in Cloud Shell, approve access, and enter the verification code in the terminal.

Download and prepare the challenge project using the bucket and project details provided by your active lab:

```bash
gcloud storage cp gs://YOUR_LAB_BUCKET/adk_project.zip .
unzip adk_project.zip
cd adk_project
pip install -r requirements.txt
```

Do not create or use API keys for this challenge. Use Agent Platform authentication as described in each task.

## Task 2: Configure the Travel Scout

The `my_google_search_agent` agent needs Google Search enabled.

1. Open `adk_project/my_google_search_agent` and edit its `.env` file. Use the project ID assigned by your active lab:

```dotenv
GOOGLE_GENAI_USE_ENTERPRISE=true
GOOGLE_CLOUD_PROJECT=YOUR_LAB_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-3.6-flash
```

2. Edit `my_google_search_agent/agent.py` and configure the agent to use the Google Search tool. Import `google_search` and pass `tools=[google_search]` to the agent definition. Ensure the instructions tell the agent to interpret and ground its responses in the search results.

3. From the project root, launch the ADK web interface with the Cloud Shell origin allowed:

```bash
cd ~/adk_project
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```

4. Open the local web server link in Cloud Shell, select `my_google_search_agent`, and ask: `What are some major events in Tokyo in 2025?` Confirm the response is grounded in Google Search results. If a request errors, try a new session.

5. Stop the web server with **Ctrl+C** and use the lab's **Check my progress** control to verify the web UI objective.

## Task 3: Verify the Travel Scout from the CLI

From the `adk_project` directory, run:

```bash
adk run my_google_search_agent
```

Ask the agent about the currency exchange rate for Japan. Verify the CLI objective with **Check my progress**, then exit with **Ctrl+C**.

## Task 4: Enforce a structured response from the Destination Verifier

The `geo_validator` agent must return a JSON object containing only the capital city.

1. Configure `geo_validator/.env` for Agent Platform, using the project ID assigned by the active lab:

```dotenv
GOOGLE_GENAI_USE_ENTERPRISE=true
GOOGLE_CLOUD_PROJECT=YOUR_LAB_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-3.6-flash
```

2. Update `geo_validator/agent.py`:
   - Define a Pydantic `CountryCapital` model that inherits from `BaseModel` and has a `capital: str` field.
   - Set `output_schema=CountryCapital` in the agent definition.
   - Set `disallow_transfer_to_parent=True` and `disallow_transfer_to_peers=True`.
   - Use the `gemini-3.6-flash` model.

3. Run the agent programmatically from the project directory:

```bash
python3 geo_validator/agent.py
```

The response should be structured JSON, for example:

```json
{"capital": "Paris"}
```

Use **Check my progress** to verify the programmatic execution objective.

## Task 5: Restore the Brochure Auditor pipeline

The `llm_auditor` workflow is intended to run two sequential stages: a Critic Agent fact-checks a claim, then a Reviser Agent corrects it. The Reviser is currently disabled.

1. Configure `llm_auditor/.env` for Agent Platform, using the project ID assigned by the active lab:

```dotenv
GOOGLE_GENAI_USE_ENTERPRISE=true
GOOGLE_CLOUD_PROJECT=YOUR_LAB_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-3.6-flash
```

2. In `llm_auditor/agent.py`, restore the Reviser Agent import and add `reviser_agent` to the sequential pipeline's `sub_agents` list after the Critic Agent.

3. From the project root, start the web interface:

```bash
cd ~/adk_project
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```

4. Select `llm_auditor` and submit this false claim:

```text
Double check this: You can take a direct train from Hawaii to Japan.
```

Confirm that the Critic debunks the claim and the Reviser provides corrected text. If needed, try a new session. Use **Check my progress** to verify the multi-agent workflow objective.

## Completion checklist

- Travel Scout searches for upcoming events and grounds its answer in Google Search.
- Travel Scout can also be run through the ADK CLI.
- Destination Verifier returns a strict JSON object with a `capital` field.
- Brochure Auditor runs both Critic and Reviser stages.
- All challenge objectives are verified in the Skills lab.

The lab uses Google Cloud resources and may incur costs. Use the active challenge's assigned project and follow its cleanup instructions when finished.
