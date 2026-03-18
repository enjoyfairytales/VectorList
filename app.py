from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev"

todos = []
next_id = 1

TRANSLATIONS = {
    "en": {
        "app_title": "Vector List",
        "eyebrow": "Local productivity",
        "subtitle": "Clean, focused task flow with instant filters.",
        "total": "Total",
        "showing": "Showing",
        "search_placeholder": "Search todos",
        "search_button": "Search",
        "search_aria": "Search todos",
        "date_aria": "Filter by date",
        "add_aria": "Add a new todo",
        "filter_all": "All",
        "filter_active": "Active",
        "filter_completed": "Completed",
        "add_placeholder": "Add a new todo",
        "add_button": "Add",
        "empty_title": "No items match this view.",
        "empty_subtitle": "Try a different filter or add a new todo.",
        "status_active": "Active",
        "status_completed": "Completed",
        "created_label": "Created",
        "complete_button": "Complete",
        "mark_active_button": "Mark active",
        "edit_button": "Edit",
        "delete_button": "Delete",
        "save_button": "Save",
        "cancel_button": "Cancel",
        "history_title": "History",
        "confirm_delete": "Delete this todo?",
        "language": "Language",
        "lang_en": "English",
        "lang_zh": "Chinese",
    },
    "zh-CN": {
        "app_title": "向量清单",
        "eyebrow": "本地效率",
        "subtitle": "清爽专注的任务流程与即时筛选。",
        "total": "总数",
        "showing": "显示",
        "search_placeholder": "搜索事项",
        "search_button": "搜索",
        "search_aria": "搜索事项",
        "date_aria": "按日期筛选",
        "add_aria": "添加新事项",
        "filter_all": "全部",
        "filter_active": "进行中",
        "filter_completed": "已完成",
        "add_placeholder": "添加新事项",
        "add_button": "添加",
        "empty_title": "当前视图没有匹配项。",
        "empty_subtitle": "尝试更换筛选条件或新增事项。",
        "status_active": "进行中",
        "status_completed": "已完成",
        "created_label": "创建于",
        "complete_button": "完成",
        "mark_active_button": "标为进行中",
        "edit_button": "编辑",
        "delete_button": "删除",
        "save_button": "保存",
        "cancel_button": "取消",
        "history_title": "历史",
        "confirm_delete": "确定删除此事项？",
        "language": "语言",
        "lang_en": "英文",
        "lang_zh": "中文",
    },
}


def _get_lang():
    requested = request.args.get("lang", "").strip()
    if requested in TRANSLATIONS:
        session["lang"] = requested
        return requested
    stored = session.get("lang")
    if stored in TRANSLATIONS:
        return stored
    return "en"


def _clean_next(raw_next: str) -> str:
    if not raw_next:
        return url_for("index")
    next_url = raw_next.strip()
    if next_url.endswith("?"):
        next_url = next_url[:-1]
    if not next_url.startswith("/"):
        return url_for("index")
    return next_url


def _find_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


def _filter_todos(q: str, status: str, created_date: str):
    q_lower = q.lower().strip()
    status_key = status or "all"
    date_key = created_date.strip()

    def matches(todo):
        if status_key == "active" and todo["completed"]:
            return False
        if status_key == "completed" and not todo["completed"]:
            return False
        if q_lower and q_lower not in todo["title"].lower():
            return False
        if date_key and todo["created_date"] != date_key:
            return False
        return True

    return [todo for todo in todos if matches(todo)]


@app.get("/")
def index():
    lang = _get_lang()
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])

    def t(key: str) -> str:
        return translations.get(key, key)

    q = request.args.get("q", "")
    status = request.args.get("status", "all")
    created_date = request.args.get("date", "")
    filtered = _filter_todos(q, status, created_date)
    return render_template(
        "index.html",
        todos=filtered,
        q=q,
        status=status,
        created_date=created_date,
        total_count=len(todos),
        lang=lang,
        t=t,
    )


@app.post("/todos")
def create_todo():
    global next_id

    title = request.form.get("title", "").strip()
    next_url = _clean_next(request.form.get("next", ""))

    if title:
        created_at = datetime.utcnow()
        todos.append(
            {
                "id": next_id,
                "title": title,
                "completed": False,
                "created_at": created_at.strftime("%Y-%m-%d %H:%M"),
                "created_date": created_at.strftime("%Y-%m-%d"),
                "history": [
                    {
                        "ts": created_at.strftime("%Y-%m-%d %H:%M"),
                        "event": "Created",
                    }
                ],
            }
        )
        next_id += 1

    return redirect(next_url)


@app.post("/todos/<int:todo_id>/toggle")
def toggle_todo(todo_id):
    todo = _find_todo(todo_id)
    next_url = _clean_next(request.form.get("next", ""))

    if todo:
        todo["completed"] = not todo["completed"]
        status_label = "Completed" if todo["completed"] else "Reopened"
        todo["history"].append(
            {
                "ts": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                "event": status_label,
            }
        )
    return redirect(next_url)


@app.post("/todos/<int:todo_id>/edit")
def edit_todo(todo_id):
    todo = _find_todo(todo_id)
    next_url = _clean_next(request.form.get("next", ""))

    if todo:
        title = request.form.get("title", "").strip()
        if title and title != todo["title"]:
            todo["title"] = title
            todo["history"].append(
                {
                    "ts": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                    "event": "Title updated",
                }
            )
    return redirect(next_url)


@app.post("/todos/<int:todo_id>/delete")
def delete_todo(todo_id):
    next_url = _clean_next(request.form.get("next", ""))
    todo = _find_todo(todo_id)
    if todo:
        todos.remove(todo)
    return redirect(next_url)


if __name__ == "__main__":
    app.run(debug=True)
