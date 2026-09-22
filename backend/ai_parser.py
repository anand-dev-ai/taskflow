import re
from datetime import date, timedelta

SYSTEM_PROMPT = """You are a task parsing assistant for TaskFlow. Convert the user's task description into a structured task."""
PRIORITY_KEYWORDS = ["urgent", "asap", "high priority", "whenever", "low priority"]
DATE_PHRASES = ["today", "tomorrow", "next week", "next monday", "next tuesday", "next wednesday", "next thursday", "next friday", "next saturday", "next sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def build_task_prompt(description: str):
    return [{"role":"system","content":SYSTEM_PROMPT.strip()},{"role":"user","content":description}]

def _next_weekday(today, target):
    days=(target-today.weekday())%7
    return today + timedelta(days=days or 7)

def normalize_due_date(hint, today=None):
    if not hint: return None
    today=today or date.today()
    hint=hint.lower()
    if hint == "today": return today
    if hint == "tomorrow": return today + timedelta(days=1)
    if hint == "next week": return today + timedelta(days=7)
    names={name:i for i,name in enumerate(["monday","tuesday","wednesday","thursday","friday","saturday","sunday"])}
    if hint.startswith("next "): return _next_weekday(today,names[hint[5:]])
    if hint in names: return _next_weekday(today,names[hint])
    return None

def parse_task_description(description: str):
    working=description.lower()
    if "urgent" in working or "asap" in working or "high priority" in working: priority="high"
    elif "whenever" in working or "low priority" in working: priority="low"
    else: priority="medium"
    matched_date=next((p for p in DATE_PHRASES if re.search(rf"\b{re.escape(p)}\b", working)), None)
    title=description
    for keyword in PRIORITY_KEYWORDS:
        title=re.sub(rf"\b{re.escape(keyword)}\b", "", title, flags=re.IGNORECASE)
    if matched_date:
        title=re.sub(rf"\b{re.escape(matched_date)}\b", "", title, flags=re.IGNORECASE)
    title=re.sub(r"\s+", " ", title).strip(" ,.-") or "Untitled task"
    return {"title":title,"priority":priority,"due_date_hint":matched_date,"due_date":normalize_due_date(matched_date)}
