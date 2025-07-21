from cli.cli_actions import (
    handle_list_tasks,
    handle_filter_tasks,
    handle_add_task,
    handle_delete_task,
    handle_mark_task,
    handle_update_task,
)
from rich.console import Console


def cli_input():
    """
    Command-line interface input loop for task manager actions.
    Shows the task list and prompts the user for an action.
    """
    actions = {
        "1": handle_filter_tasks,
        "2": handle_add_task,
        "3": handle_update_task,
        "4": handle_mark_task,
        "5": handle_delete_task,
    }
    console = Console()
    import shutil
    while True:
        handle_list_tasks()
        width = shutil.get_terminal_size((80, 20)).columns
        prompt_raw = "Select action (1-6): "
        styled_prompt = f"[bold white]{prompt_raw}[/]"
        pad = max((width - len(prompt_raw)) // 2, 0)
        user_input = console.input(" " * pad + styled_prompt).strip()
        if user_input in actions:
            actions[user_input]()
        elif user_input == "6":
            console.print("[bold magenta]Exiting... Goodbye![/]")
            break
        else:
            console.print("[bold red]Enter a valid number between 1 and 6.[/]")
