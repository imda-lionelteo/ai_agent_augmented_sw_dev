from src.sw_architect.workflow import run_workflow


def main() -> None:
    """
    Main entry point for the Software Architect workflow application.

    Initiates the requirements analysis workflow by triggering the multi-agent
    system to analyze Jira data and generate comprehensive architectural documentation.
    The workflow extracts epics, stories, and tasks from the Jira data source and
    produces structured requirements analysis output.
    """
    # Execute the Software Architect workflow to analyze requirements from Jira data
    run_workflow("Analyze requirements for project")


if __name__ == "__main__":
    main()
