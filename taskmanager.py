# File: task_manager.py

import sqlite3
import re

# Database setup
def initialize_db():
    """Create the DB and the tables for this app if they do not exist already"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT,
            deadline TEXT,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

def add_task(description, category=None, deadline=None):
    """
    Add a new task to the database.

    :param description: Task description.
    :param category: Optional category of the task.
    :param deadline: Optional deadline in YYYY-MM-DD format.
    """
    if not description:
        print("Description cannot be empty.")
        return
    if deadline and not re.match(r'\d{4}-\d{2}-\d{2}', deadline):
        print("Invalid deadline format. Use YYYY-MM-DD.")
        return

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (description, category, deadline, completed)
        VALUES (?, ?, ?, ?)
    ''', (description, category, deadline, False))
    conn.commit()
    conn.close()

def list_tasks(sort_by=None):
    """List all tasks in DB. No parameters"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    query = 'SELECT * FROM tasks'
    if sort_by == 'deadline':
        query += ' ORDER BY deadline'
    elif sort_by == 'status':
        query += ' ORDER BY completed'
    c.execute(query)
    tasks = c.fetchall()
    if not tasks:
        print("No tasks found!")
    else:
        for task in tasks:
            status = "✓" if task[4] else "✗"
            print(f"ID: {task[0]} | Description: {task[1]} | Category: {task[2]} | Deadline: {task[3]} | Status: {status}")
    conn.close()

def remove_task(task_id):
    """
    Remove a task from the database by ID.

    :param task_id: ID of the task to be removed.
    """
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    if c.rowcount == 0:
        print("Task ID not found.")
    else:
        print("Task removed.")
    conn.commit()
    conn.close()

def mark_task_completed(task_id):
    """
    Mark a task as completed by ID.

    :param task_id: ID of the task to be marked as completed.
    """
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
    conn.commit()
    conn.close()

def search_tasks(category=None, deadline=None):
    """
    Search for tasks by category and/or deadline.

    :param category: Optional category to filter by.
    :param deadline: Optional deadline to filter by.
    """
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    query = 'SELECT * FROM tasks WHERE 1=1'
    params = []
    if category:
        query += ' AND category = ?'
        params.append(category)
    if deadline:
        query += ' AND deadline = ?'
        params.append(deadline)
    c.execute(query, params)
    tasks = c.fetchall()
    if not tasks:
        print("No tasks found!")
    else:
        for task in tasks:
            status = "✓" if task[4] else "✗"
            print(f"ID: {task[0]} | Description: {task[1]} | Category: {task[2]} | Deadline: {task[3]} | Status: {status}")
    conn.close()

def update_task(task_id, description=None, category=None, deadline=None):
    """
    Update the details of a task.

    :param task_id: ID of the task to be updated.
    :param description: New description for the task.
    :param category: New category for the task.
    :param deadline: New deadline for the task.
    """
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if description:
        c.execute('UPDATE tasks SET description = ? WHERE id = ?', (description, task_id))
    if category:
        c.execute('UPDATE tasks SET category = ? WHERE id = ?', (category, task_id))
    if deadline:
        if not re.match(r'\d{4}-\d{2}-\d{2}', deadline):
            print("Invalid deadline format. Use YYYY-MM-DD.")
            conn.close()
            return
        c.execute('UPDATE tasks SET deadline = ? WHERE id = ?', (deadline, task_id))
    if c.rowcount == 0:
        print("Task ID not found.")
    else:
        print("Task updated.")
    conn.commit()
    conn.close()

def task_summary():
    """Display a summary of tasks: total, completed, and pending."""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM tasks')
    total_tasks = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tasks WHERE completed = ?', (True,))
    completed_tasks = c.fetchone()[0]
    pending_tasks = total_tasks - completed_tasks
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Pending tasks: {pending_tasks}")
    conn.close()

def main():
    """The main function"""
    initialize_db()
    print("Welcome to tasker, an easy-to-use task manager")
    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Remove Task")
        print("4. Mark Task as Completed")
        print("5. Search Tasks")
        print("6. Update Task")
        print("7. Task Summary")
        print("8. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            description = input("Enter task description: ")
            category = input("Enter task category (optional): ")
            deadline = input("Enter task deadline (optional, YYYY-MM-DD): ")
            add_task(description, category, deadline)
        elif choice == '2':
            sort_option = input("Sort by (deadline/status/none): ").strip().lower()
            if sort_option not in ['deadline', 'status', 'none']:
                print("Invalid sort option.")
                continue
            list_tasks(sort_by='deadline' if sort_option == 'deadline' else 'status' if sort_option == 'status' else None)
        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to remove: "))
                remove_task(task_id)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to mark as completed: "))
                mark_task_completed(task_id)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif choice == '5':
            category = input("Enter category to search (optional): ")
            deadline = input("Enter deadline to search (optional, YYYY-MM-DD): ")
            search_tasks(category, deadline)
        elif choice == '6':
            try:
                task_id = int(input("Enter task ID to update: "))
                description = input("Enter new description (optional): ")
                category = input("Enter new category (optional): ")
                deadline = input("Enter new deadline (optional, YYYY-MM-DD): ")
                update_task(task_id, description, category, deadline)
            except ValueError:
                print("Invalid input. Enter a number.")
        elif choice == '7':
            task_summary()
        elif choice == '8':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
