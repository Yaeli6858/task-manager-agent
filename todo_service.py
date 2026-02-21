from datetime import datetime

tasks = []
next_id = 1


def get_tasks(filters=None):
    return tasks


def add_task(title="New Task", description="", task_type="general"):
    global next_id
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "type": task_type,
        "start_date": datetime.now().isoformat(),
        "end_date": None,
        "status": "open"
    }
    tasks.append(task)
    next_id += 1
    return task


def update_task(task_id, status="done"):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            return task
    return None


def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return True