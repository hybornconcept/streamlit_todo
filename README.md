
# 📝 Task Manager Pro

![Task Manager Pro](https://img.shields.io/badge/Streamlit-Task%20Manager-FF4B4B?style=for-the-badge&logo=streamlit)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://task-manager-pro.streamlit.app)

A modern, intuitive task management application built with Streamlit and SQLite. Task Manager Pro combines powerful features with a beautiful, user-friendly interface to help you stay organized and boost productivity.

## 🌟 Why Task Manager Pro?

- **Elegant Simplicity**: Clean, modern interface that puts your tasks front and center
- **Real-time Updates**: Changes reflect instantly without page reloads
- **Data Persistence**: Secure SQLite backend ensures your tasks are safely stored
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Zero Configuration**: Get started in seconds with no complex setup

## 🎯 Core Features

### Task Management
- ✨ Create, edit, and delete tasks with ease
- 📅 Set and track deadlines
- 📝 Add detailed notes and descriptions
- ✅ Mark tasks as complete/incomplete
- 🔄 Real-time task updates

### User Interface
- 🎨 Clean, modern design with customizable themes
- 📱 Responsive layout for all screen sizes
- 🚀 Smooth animations and transitions
- ⚡ Lightning-fast performance
- 🌙 Dark/Light mode support

### Data Management
- 💾 Automatic data persistence with SQLite
- 🔒 Secure data storage
- 🔄 Automatic state management
- 📊 Session state debugging tools
- 🔍 Easy data inspection

## 🛠️ Technical Architecture

### Frontend (Streamlit)
- Streamlit components for UI rendering
- Session state management for data persistence
- Fragment-based UI updates for performance
- Form handling and validation
- Real-time UI updates

### Backend (SQLite + SQLAlchemy)
- SQLite database for data storage
- SQLAlchemy ORM for database operations
- Connection pooling and management
- Transaction handling
- Data validation and integrity checks

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-manager-pro.git
cd task-manager-pro
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
```bash
# Create .streamlit/secrets.toml with:
[connections.task_db]
type = "sql"
url = "sqlite:///task.db"
```

5. Run the application:
```bash
streamlit run streamlit_app.py
```

## 🔧 Configuration

### Environment Variables
- `STREAMLIT_THEME_BASE`: Set UI theme (light/dark)
- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Host address (default: localhost)

### Database Configuration
Database settings can be modified in `.streamlit/secrets.toml`:
```toml
[connections.task_db]
type = "sql"
url = "sqlite:///task.db"
```

## 🚀 Usage

1. **Creating Tasks**
   - Click "New Task" button
   - Enter task name, description, and deadline
   - Click "Add Task" to save

2. **Managing Tasks**
   - Click "Edit" to modify task details
   - Use "Complete" to mark tasks as done
   - Click "Delete" to remove tasks

3. **Organizing Tasks**
   - Tasks are automatically sorted by creation date
   - Completed tasks are visually distinguished
   - Deadline indicators show task urgency

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the Apache License 2.0. See `LICENSE` for more information.

## 👏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database operations
- [SQLite](https://www.sqlite.org/) for reliable data storage

## 📫 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/task-manager-pro](https://github.com/yourusername/task-manager-pro)

---

<p align="center">Made with ❤️ by HYBORN</p>
