"""
Complete example: Running an ADK agent programmatically
"""

# Step 1: Install ADK (run this in terminal or notebook cell)
# pip install google-adk

# Step 2: Configure Environment & Backend
import os

# Option A: Gemini Developer API (AI Studio) 
# os.environ['GOOGLE_API_KEY'] = 'your-api-key-here' 
# os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'FALSE' 

# Option B: Gemini platform backend 
# os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'TRUE' 
# os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-gcp-project-id' 
# os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1' 
# (Ensure Google Cloud ADC is authenticated via: gcloud auth application-default login) 

# Step 3: Import required libraries
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Step 4: Define your agent
agent = Agent(
    model="gemini-flash-latest",
    name="math_tutor",
    instruction="""You are a patient math tutor.
    Guide students through problems step-by-step.
    Don’t just give answers - help them discover solutions."""
)

# Step 5: Set up session and runner
APP_NAME = "math_tutor_app"
USER_ID = "student_1"
SESSION_ID = "session_001"

session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service
)

# Step 6: Define async function to run the agent
async def run_agent():
    # Create session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: {SESSION_ID}\n")

    # Prepare user message
    user_message = Content(
        role="user",
        parts=[Part(text="How do I solve 2x + 5 = 13?")]
    )

    # Run agent and collect response
    print("User: How do I solve 2x + 5 = 13?\n")
    print("Agent: ", end="")

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message
    ):
        # Print final response
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)

# Step 7: Run the agent
# For Jupyter/Colab: Use await directly
# await run_agent()

# For Python scripts: Use asyncio.run()
if __name__ == "__main__":
    asyncio.run(run_agent())
