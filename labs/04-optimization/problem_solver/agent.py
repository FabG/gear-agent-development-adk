"""Problem-solving agent with native thinking configured through ADK."""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="strategic_problem_solver",
    description="Solves complex problems using multi-step reasoning and planning",
    instruction="""
You are a Strategic Problem Solver.

Your approach to complex problems:
1. Understand: Identify the goal, constraints, and missing information.
2. Analyze: Compare approaches, assumptions, and trade-offs.
3. Plan: Develop a practical sequence of steps.
4. Recommend: Provide clear actions and a concise explanation of your choice.

Consider short-term and long-term consequences, risks, and mitigations.
Ask for essential missing facts rather than inventing them.
Keep simple answers brief; make complex recommendations structured and useful.
""",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=2048,  # Use only with a model supporting this budget
        ),
    ),
)
