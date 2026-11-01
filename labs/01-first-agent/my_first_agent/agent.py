from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-flash-latest',
    name='math_tutor_agent',
    description='Helps students learn algebra by guiding them through problem-solving steps.',
    instruction='You are a patient math tutor. Help students with algebra problems.',
)
original_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

