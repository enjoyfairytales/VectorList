# VectorList ✅

VectorList is a lightweight Flask app for managing a clean, focused todo list with instant filters and a bilingual UI.
VectorList 是一个轻量级 Flask 待办应用，主打清爽专注的任务流、即时筛选与中英双语界面。

## Features ✨
- Create, edit, complete, and delete todos
- Filter by status (all/active/completed)
- Search by text and filter by creation date
- Per-item history timeline (created, completed, reopened, title updates)
- English and Chinese UI switch

## 功能亮点 ✨
- 支持新增、编辑、完成与删除事项
- 状态筛选（全部/进行中/已完成）
- 文本搜索 + 创建日期筛选
- 每条事项自带历史记录（创建/完成/重开/改标题）
- 中英文界面一键切换

## Tech Stack 🧰
- Python + Flask
- Server-rendered HTML/CSS with a small vanilla JS helper
- In-memory data store (resets on restart)

## 技术栈 🧰
- Python + Flask
- 服务端渲染 HTML/CSS + 少量原生 JS
- 内存存储（重启后清空）

## Local Setup 🚀
1. Create a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install flask
```

3. Run the app:

```bash
python app.py
```

4. Open the app:

```
http://127.0.0.1:5000/
```

## Project Structure 🗂️
- `app.py` - Flask routes, translations, and in-memory todo logic
- `templates/index.html` - Main page template
- `static/styles.css` - App styles
- `static/app.js` - Edit toggles + delete confirmation

## 项目结构 🗂️
- `app.py` - Flask 路由、翻译与内存待办逻辑
- `templates/index.html` - 主页面模板
- `static/styles.css` - 样式文件
- `static/app.js` - 编辑切换 + 删除确认

## Notes ⚠️
- Todos live in memory; restarting the server clears all items.
- The `lang` query param controls language selection (persisted in session).

## 说明 ⚠️
- 待办存储在内存中，重启会清空。
- `lang` 查询参数控制语言，且会写入 session。
