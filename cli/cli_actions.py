import shutil
from datetime import datetime, date
from core.task import Task
from core.manager import TaskManager
from data.db import execute_psql
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.align import Align

manager = TaskManager()


def handle_list_tasks() -> None:  # List Tasks
    rows = manager.list_tasks()
    console = Console()

    table = Table(
        title="[bold italic underline]CLI Task Manager[/]",
        box=box.SIMPLE_HEAVY
    )

    table.add_column("ID", justify="center",
                     style="bold cyan", header_style="bold cyan")
    table.add_column("Title", justify="left",
                     style="bold italic yellow", header_style="bold yellow")
    table.add_column("Description", justify="left",
                     style="white", header_style="bold white")
    table.add_column("Due Date", justify="left",
                     style="white", header_style="bold white")
    table.add_column("Priority", justify="right",
                     style="bold magenta", header_style="bold white")
    table.add_column("Status", justify="right",
                     style="bold blue", header_style="bold white")
    table.add_column("Timestamp", justify="right",
                     style="dim", header_style="bold white")

    for row in rows:
        priority_style = {
            "Low": "dim orange4",
            "Medium": "dim orange1",
            "High": "bold red3"
        }.get(str(row.priority), "white")

        status_style = {
            "Pending": "dim orange1",
            "WIP": "dim chartreuse2",
            "Done": "bold green1",
        }.get(str(row.status), "white")

        timestamp = (
            f"{row.created_at.strftime('%b %d, %Y')} "
            f"{row.created_at.strftime('%I:%M %p')}"
            if hasattr(row.created_at, 'strftime')
            else str(row.created_at)
        )
        due_date_str = (
            row.due_date.strftime('%b %d, %Y')
            if hasattr(row.due_date, 'strftime')
            else str(row.due_date)
        )
        title_str = f"[bold italic underline yellow]{row.title}[/]"

        table.add_row(
            str(row.id),
            title_str,
            str(row.description),
            due_date_str,
            f"[{priority_style}]{row.priority}[/]",
            f"[{status_style}]{row.status}[/]",
            timestamp
        )

    actions_text = (
        "[bold white] 1:Filter │ 2:Add │ 3:Update │ 4:Complete "
        "│ 5:Delete │ 6:Exit [/]"
    )
    footer_panel = Panel(
        Align.center(actions_text),
        padding=(0, 1),
        box=box.MINIMAL,
        style=""
    )

    console.print(Align.center(table))
    console.print(Align.center(footer_panel))


def centered_input(prompt_raw, style="bold white"):
    console = Console()
    width = shutil.get_terminal_size((80, 20)).columns
    styled_prompt = f"[{style}]{prompt_raw}[/]"
    pad = max((width - len(prompt_raw)) // 2, 0)
    return console.input(" " * pad + styled_prompt).strip()


def handle_add_task() -> None:  # Add Task
    console = Console()
    title = centered_input("Title:", "bold yellow")
    if not title:
        console.print(Align.center("[bold red]Task cannot be empty.[/]"))
        return
    description = centered_input("Description (optional):") or None
    due = centered_input("Due Date (YYYY-MM-DD) or blank:", "white")
    priority = centered_input("Priority (Low/Medium/High):") or "Medium"
    if priority not in {"Low", "Medium", "High"}:
        console.print(Align.center("[bold red]Invalid priority.[/]"))
        priority = "Medium"
    status = "Pending"

    due_date = parse_date(due)

    task = Task(title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status)
    manager.add_task(task)
    console.print("[bold green]Task added![/]")


def parse_date(date_str: str) -> date | None:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format (YYYY-MM-DD).")
        return None


def validate_task_id(task_id: int) -> int | None:
    if not isinstance(task_id, int):
        print("Task ID must be an integer.")
        return None

    query = "SELECT 1 FROM tasks WHERE id = %s LIMIT 1;"
    result = execute_psql(query, params=(task_id,), fetch_results=True)

    if not result:
        print(f"Task ID {task_id} does not exist.")
        return None

    return task_id


def handle_filter_tasks() -> None:  # List Tasks w/ Filter
    console = Console()
    width = shutil.get_terminal_size((80, 20)).columns
    console.print("\n")
    filter_msg = "Leave empty to skip filtering by column."
    pad_msg = max((width - len(filter_msg)) // 2, 0)
    console.print(" " * pad_msg + f"[bold white]{filter_msg}[/]\n")

    due_date = centered_input("Due Date (YYYY-MM-DD): ")
    priority = centered_input("Priority (Low/Medium/High): ").capitalize()
    status = centered_input("Status (Pending/WIP/Done): ")

    fields = {
        "due_date": due_date,
        "priority": priority,
        "status": status,
    }

    filters = {key: value for key, value in fields.items() if value}

    if filters:
        manager.filter_tasks(filters)
    else:
        no_filter_msg = "No filters applied."
        pad_no = max((width - len(no_filter_msg)) // 2, 0)
        console.print(" " * pad_no + f"[bold yellow]{no_filter_msg}[/]")


def handle_update_task() -> None:
    console = Console()
    try:
        raw_id = int(centered_input("Task ID to update:", "bold cyan"))
    except ValueError:
        console.print(Align.center("[bold red]Task ID should be integer.[/]"))
        return

    task_id = validate_task_id(raw_id)
    if task_id is None:
        return

    console.print("[bold white]Leave empty to skip updating a field.[/]")

    fields = {
        "title": centered_input("Title:", "bold yellow"),
        "description": centered_input("Description:"),
        "due_date": centered_input("Due Date (YYYY-MM-DD):", "white"),
        "priority": centered_input("Priority (Low/Medium/High):").capitalize(),
        "status": centered_input("Status (Pending/WIP/Done):")
    }

    updates = {key: value for key, value in fields.items() if value}
    manager.update_task(raw_id, updates)
    console.print(f"[bold green]Task {raw_id} updated![/]")


def handle_mark_task() -> None:
    console = Console()
    try:
        raw_id = int(centered_input(
            "Task ID to mark as completed:", "bold cyan"
        ))
    except ValueError:
        console.print(Align.center("[bold red]Task ID must be an integer.[/]"))
        return

    task_id = validate_task_id(raw_id)
    if task_id is None:
        return

    manager.mark_task(task_id)
    console.print(f"[bold green]Task ID {task_id} marked as completed.[/]")


def handle_delete_task() -> None:
    from rich.prompt import Confirm
    console = Console()
    try:
        raw_id = int(centered_input("Task ID to delete:", "bold cyan"))
    except ValueError:
        console.print(Align.center("[bold red]Task ID must be an integer.[/]"))
        return

    task_id = validate_task_id(raw_id)
    if task_id is None:
        return

    answer = Confirm.ask(f"[bold red]Delete [bold cyan]{task_id}[/]?[/]")
    if answer:
        manager.delete_task(task_id)
        console.print(f"[bold green]Task ID {task_id} deleted.[/]")
    else:
        console.print("[bold yellow]Task deletion canceled.[/]")
