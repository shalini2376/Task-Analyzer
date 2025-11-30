from datetime import date, datetime
from typing import Any, Dict, Optional, List


def _parse_due_date(raw_due_date: Any) -> Optional[date]:
    """
    Helper: accepts either a date object or a 'YYYY-MM-DD' string.
    Returns a date object or None if invalid.
    """
    if isinstance(raw_due_date, date):
        return raw_due_date

    if isinstance(raw_due_date, str):
        # Adjust format if you decide to send different date formats from frontend
        try:
            return datetime.strptime(raw_due_date, "%Y-%m-%d").date()
        except ValueError:
            return None

    return None


def calculate_task_score(task_data: Dict[str, Any]) -> int:
    """
    Calculates a priority score for a task.
    Higher score = higher priority.

    Expected keys in task_data:
    - title (str)
    - due_date (date or 'YYYY-MM-DD' string)
    - importance (int 1–10)
    - estimated_hours (int)
    - dependencies (list)
    """
    score = 0

    today = date.today()

    # -------------------------
    # 1. Urgency (based on due_date)
    # -------------------------
    raw_due_date = task_data.get("due_date")
    due_date_obj = _parse_due_date(raw_due_date)

    if due_date_obj is None:
        # If date is missing/invalid, we treat it as "no urgency"
        days_until_due = None
    else:
        days_until_due = (due_date_obj - today).days

    if days_until_due is not None:
        if days_until_due < 0:
            # Overdue = very high priority
            score += 80
        elif days_until_due <= 1:
            # due today or tomorrow
            score += 60
        elif days_until_due <= 3:
            score += 40
        elif days_until_due <= 7:
            score += 20
        # else: more than a week away → no urgency bonus

    # -------------------------
    # 2. Importance
    # -------------------------
    importance = task_data.get("importance", 5)

    # Clamp importance into [1, 10]
    try:
        importance = int(importance)
    except (TypeError, ValueError):
        importance = 5  # fallback default

    if importance < 1:
        importance = 1
    if importance > 10:
        importance = 10

    # Give importance a strong weight
    score += importance * 7

    # -------------------------
    # 3. Effort (estimated_hours)
    # -------------------------
    estimated_hours = task_data.get("estimated_hours", 1)
    try:
        estimated_hours = int(estimated_hours)
    except (TypeError, ValueError):
        estimated_hours = 1

    # Quick wins logic
    if estimated_hours <= 1:
        score += 20     # very quick
    elif estimated_hours <= 3:
        score += 10     # still manageable
    elif estimated_hours >= 8:
        score -= 10     # big heavy tasks get slight penalty

    # -------------------------
    # 4. Dependencies
    # -------------------------
    dependencies: List[Any] = task_data.get("dependencies") or []

    # If there are dependencies, slightly reduce priority
    # assuming they might not be immediately actionable.
    if len(dependencies) > 0:
        score -= 15

    return score
