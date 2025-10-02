"""
Software Architect Workflow Module

This module defines the multi-agent workflow for software requirements extraction and architectural analysis.
It coordinates AI agents to process user input and generate comprehensive software architecture documentation.
"""

from pathlib import Path

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file import FileTools
from agno.workflow.workflow import Workflow

from src.sw_architect.instructions import (
    REQUIREMENTS_ANALYSIS_INSTRUCTIONS,
)
from src.tools.simulate_jira_tool import simulate_jira_tool

# ===============================
# Agents
# ===============================
# Requirements Analysis Agent: Extracts and analyzes software requirements from user input
# Uses JIRA simulation tools and file operations to gather and document requirements
requirements_analysis_agent: Agent = Agent(
    name="Requirements Analysis Agent",
    model=OpenAIChat(
        id="gpt-4o-mini",
    ),
    tools=[simulate_jira_tool, FileTools(base_dir=Path("tmp"))],
    instructions=REQUIREMENTS_ANALYSIS_INSTRUCTIONS,
)


# ===============================
# Workflow
# ===============================
def run_workflow(input: str) -> None:
    """
    Execute the Software Architect Workflow.

    This function initializes and runs a multi-agent workflow that processes user input
    to extract requirements and perform architectural analysis. The workflow uses persistent
    storage to track sessions and streams responses in real-time.

    Args:
        input (str): The user's input containing software requirements or architectural questions

    Returns:
        None: Results are streamed to stdout in markdown format
    """
    software_architect_workflow: Workflow = Workflow(
        name="Software Architect Workflow",
        description="Automated multi-agent workflow for software requirements extraction and architectural analysis",
        steps=[requirements_analysis_agent],
    )

    # Execute the workflow
    software_architect_workflow.print_response(input, markdown=True)
