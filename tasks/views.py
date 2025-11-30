import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import date
from .scoring import calculate_task_score, _parse_due_date

def index(request):
    return render(request, "index.html")

@csrf_exempt
def analyze_tasks(request):
    """
    Accepts a POST request with JSON containing a list of tasks.
    Returns the same tasks sorted by their calculated score.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        # Convert request body (bytes) → Python list
        tasks = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not isinstance(tasks, list):
        return JsonResponse({"error": "Data must be an array of tasks"}, status=400)

    scored_tasks = []

    for task in tasks:
        # Calculate score for each task
        score = calculate_task_score(task)
        task["score"] = score
        scored_tasks.append(task)

    # Sort tasks by highest score
    scored_tasks.sort(key=lambda x: x["score"], reverse=True)

    return JsonResponse(scored_tasks, safe=False)

@csrf_exempt
def suggest_tasks(request):
    """
    Accepts a POST request with JSON containing a list of tasks.
    Returns the top 3 tasks to focus on "today",
    with an explanation string for each.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        tasks = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not isinstance(tasks, list):
        return JsonResponse({"error": "Data must be an array of tasks"}, status=400)

    today = date.today()
    scored_tasks = []

    for task in tasks:
        score = calculate_task_score(task)
        task["score"] = score

        # Parse due date for today/overdue logic
        due_date_obj = _parse_due_date(task.get("due_date"))

        # Build a human-readable explanation
        reasons = []

        if due_date_obj is not None:
            days_until_due = (due_date_obj - today).days

            if days_until_due < 0:
                reasons.append("This task is overdue.")
            elif days_until_due == 0:
                reasons.append("This task is due today.")
            elif days_until_due <= 3:
                reasons.append("This task is due soon.")
            else:
                reasons.append(f"This task is due in {days_until_due} days.")
        else:
            reasons.append("No valid due date provided.")

        importance = task.get("importance", 5)
        try:
            importance = int(importance)
        except (TypeError, ValueError):
            importance = 5

        if importance >= 8:
            reasons.append("It has very high importance.")
        elif importance >= 5:
            reasons.append("It has medium importance.")
        else:
            reasons.append("It has low importance.")

        estimated_hours = task.get("estimated_hours", 1)
        try:
            estimated_hours = int(estimated_hours)
        except (TypeError, ValueError):
            estimated_hours = 1

        if estimated_hours <= 1:
            reasons.append("It's a quick win (takes about 1 hour or less).")
        elif estimated_hours <= 3:
            reasons.append("It is manageable within a few hours.")
        else:
            reasons.append("It may take significant time to complete.")

        dependencies = task.get("dependencies") or []
        if dependencies:
            reasons.append("However, it has dependencies that might block you.")
        else:
            reasons.append("It has no dependencies, so you can start right away.")

        # Join reasons into a single explanation string
        task["explanation"] = " ".join(reasons)

        scored_tasks.append(task)

    # Prefer tasks that are overdue or due today
    today_or_overdue = []
    future_tasks = []

    for task in scored_tasks:
        due_date_obj = _parse_due_date(task.get("due_date"))
        if due_date_obj is not None and due_date_obj <= today:
            today_or_overdue.append(task)
        else:
            future_tasks.append(task)

    # Sort both groups by score desc
    today_or_overdue.sort(key=lambda x: x["score"], reverse=True)
    future_tasks.sort(key=lambda x: x["score"], reverse=True)

    # Pick top 3, preferring today/overdue
    suggested = today_or_overdue[:3]
    if len(suggested) < 3:
        remaining_slots = 3 - len(suggested)
        suggested.extend(future_tasks[:remaining_slots])

    return JsonResponse(suggested, safe=False)
