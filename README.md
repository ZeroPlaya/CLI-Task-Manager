# CLI Task Manager

A command-line tool built with Python and PostgreSQL for exploring how to manage tasks via the terminal. This project is meant for practice and experimentation and is not intended for practical use.

---

## Features

- Add new tasks with title, description, due date, priority, and status  
- List all tasks or filter tasks by priority, due date, or status  
- Update task details  
- Mark tasks as completed  
- Delete tasks  
- Data persists in a **PostgreSQL** database  
- Easy-to-use command-line interface (CLI)  

---

## Setup Instructions

1. **Install Python dependencies**  
Open your terminal or command prompt and run:  
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**  
Create a `.env` file in the project root with your PostgreSQL credentials:
```
DB_HOST=your_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

3. **Run the app**  
The database table will be created automatically at startup if it doesn't exist.  
Run the CLI Task Manager:
```bash
python main.py
```

## Project Goals

- [x] ~~Refactor architecture~~  
  - [x] ~~Improve modularity~~  
  - [x] ~~Ensure meaningful return values~~  
- [ ] Input validation and error handling  
  - [ ] Validate input types and formats  
  - [x] ~~Handle exceptions and edge cases~~  
- [ ] Task Features  
  - [x] ~~Search by keyword (title/description)~~  
  - [ ] Export tasks (CSV, JSON)  
  - [ ] Add categories/tags  
  - [ ] Undo/redo functionality  


### Development & Testing

- [ ] Testing  
  - [ ] Unit tests for core modules  
  - [ ] Integration tests for workflows  
- [ ] CLI Improvements  
  - [ ] Command aliases (`ls`, `del`, etc.)  
  - [ ] Interactive CLI interface  
- [ ] Deployment  
  - [ ] Docker containerization  
  - [ ] Cloud/API sync  

