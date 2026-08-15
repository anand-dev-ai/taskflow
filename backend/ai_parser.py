import re

SYSTEM_PROMPT = """
You are a task parsing assistant for TaskFlow.
Convert the user's task description into a structured task.
Determine the priority, title, and due-date hint according to
the TaskFlow parsing rules.
Return only structured task information.
"""


def build_task_prompt(description: str):
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.strip()
        },
        {
            "role": "user",
            "content": description
        }
    ]

PRIORITY_KEYWORDS = [
    "urgent",
    "asap",
    "whenever",
    "low priority",
]

DATE_PHRASES = [
    "today",
    "tomorrow",
    "next week",
    "next monday",
    "next tuesday",
    "next wednesday",
    "next thursday",
    "next friday",
    "next saturday",
    "next sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def parse_task_description(description: str):
    """
    Deterministic TaskFlow quick-add parser.

    Returns:
        {
            "title": str,
            "priority": str,
            "due_date_hint": str | None
        }
    """

    working = description.lower()

    # -------------------------------------------------
    # Priority
    # -------------------------------------------------

    if "urgent" in working or "asap" in working:
        priority = "high"

    elif "whenever" in working or "low priority" in working:
        priority = "low"

    else:
        priority = "medium"

    # -------------------------------------------------
    # Due-date hint
    # -------------------------------------------------

    matched_date = None

    for phrase in DATE_PHRASES:
        if phrase in working:
            matched_date = phrase
            break

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    title = description

    # Remove every priority keyword occurrence.
    for keyword in PRIORITY_KEYWORDS:
        title = re.sub(
            re.escape(keyword),
            "",
            title,
            flags=re.IGNORECASE
        )

    # Remove every occurrence of the matched date phrase.
        # Remove every occurrence of the matched date phrase.
    if matched_date is not None:
        title = re.sub(
            re.escape(matched_date),
            "",
            title,
            flags=re.IGNORECASE
        )

    title = re.sub(r"\s+", " ", title).strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": matched_date
    }