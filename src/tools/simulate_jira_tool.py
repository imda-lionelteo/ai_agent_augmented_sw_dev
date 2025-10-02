from pathlib import Path

from agno.tools import tool
from pydantic import BaseModel


class JiraTask(BaseModel):
    """
    Represents a Jira task with all relevant fields.

    This model defines the structure for individual Jira tasks extracted from the
    jira_data.json file. Tasks represent granular work items that comprise user stories,
    including implementation, testing, and quality assurance activities.

    Attributes:
        task_id: Unique identifier for the Jira task (e.g., US-TASK-028, US-TASK-029)
        summary: Brief one-line summary of the task
        description: Detailed description explaining the task requirements and deliverables
        acceptance_criteria: List of conditions that must be met for task completion
        priority: Priority level (e.g., High, Medium, Low, Critical)
        status: Current workflow status (e.g., To Do, In Progress, Done, Blocked)
        assignee: User identifier of the person assigned to the task (or "Unassigned")
        reporter: User identifier of the person who created the task
        created: ISO 8601 timestamp of task creation
        updated: ISO 8601 timestamp of last update
    """

    task_id: str
    summary: str
    description: str
    acceptance_criteria: list[str]
    priority: str
    status: str
    assignee: str
    reporter: str
    created: str
    updated: str


class JiraStory(BaseModel):
    """
    Represents a Jira user story with comprehensive metadata for requirements analysis.

    User stories are the primary units of work extracted from the jira_data.json file.
    Each story captures functional requirements, acceptance criteria, and technical
    implementation details that inform architectural decisions and system design.
    Stories are organized under epics and contain multiple tasks for implementation.

    Attributes:
        story_id: Unique identifier for the user story (e.g., US-R10, US-R11)
        name: Concise story title describing the feature or capability
        description: Complete user story narrative in "As a [role], I want [goal],
                    so that [benefit]" format
        acceptance_criteria: List of testable conditions that define story completion
        technical_notes: Implementation guidance, technology choices, security considerations,
                        and architectural constraints
        dependencies: List of prerequisite story IDs that must be completed first
        effort: Estimated implementation effort (S/M/L sizing)
        tasks: List of JiraTask objects representing implementation, testing, and QA subtasks
    """

    story_id: str
    name: str
    description: str
    acceptance_criteria: list[str]
    technical_notes: list[str]
    dependencies: list[str]
    effort: str
    tasks: list[JiraTask]


class JiraEpic(BaseModel):
    """
    Represents a Jira epic containing a collection of related user stories.

    Epics provide high-level organization of work around major features, capabilities,
    or business objectives. The epic structure establishes the hierarchical framework
    for requirements analysis, helping to identify cross-cutting concerns, integration
    points, and architectural patterns needed across multiple stories.

    Attributes:
        epic_id: Unique identifier for the epic (e.g., Epic 1, Epic 2)
        name: Descriptive epic name reflecting the major feature or capability
        description: High-level overview explaining the epic's purpose and scope
        key_objectives: List of strategic goals and success criteria for the epic
        stories: List of JiraStory objects that comprise this epic
    """

    epic_id: str
    name: str
    description: str
    key_objectives: list[str]
    stories: list[JiraStory]


class JiraResponse(BaseModel):
    """
    Response schema for structured Jira data extraction and requirements analysis.

    This model defines the complete output structure of the jira_epics_agent, which
    parses the jira_data.json file and transforms it into a hierarchical data structure.
    The extracted information includes epics, stories, tasks, acceptance criteria,
    technical notes, and dependencies, all of which feed into the requirements_analysis_agent
    for comprehensive architectural analysis and documentation.

    Attributes:
        epics: List of JiraEpic objects representing the complete project epic hierarchy
    """

    epics: list[JiraEpic]


@tool()
def simulate_jira_tool() -> JiraResponse:
    """
    Simulates reading Jira data from a JSON file and parses it into JiraResponse.

    Returns:
        JiraResponse object containing Jira epics, stories, and tasks data
    """
    import json

    file_path = Path("data/jira_data.json")
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json_content = f.read()

        data = json.loads(json_content)
        return JiraResponse(**data)

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {str(e)}")
