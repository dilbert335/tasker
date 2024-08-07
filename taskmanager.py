import sqlite3

# Database!
def initialize_db():
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
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (description, category, deadline, completed)
        VALUES (?, ?, ?, ?)
    ''', (description, category, deadline, False))
    conn.commit()
    conn.close()

def list_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    for task in tasks:
        status = "✓" if task[4] else "✗"
        print(f"ID: {task[0]} | Description: {task[1]} | Category: {task[2]} | Deadline: {task[3]} | Status: {status}")
    conn.close()

def remove_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def mark_task_completed(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
    conn.commit()
    conn.close()

def main():
    initialize_db()
    print("Welcome to tasker, an easy to use task manager")
    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Remove Task")
        print("4. Mark Task as Completed")
        print("5. Search Tasks")
        print("6. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            description = input("Enter task description: ")
            category = input("Enter task category (optional): ")
            deadline = input("Enter task deadline (optional, YYYY-MM-DD): ")
            add_task(description, category, deadline)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = int(input("Enter task ID to remove: "))
            remove_task(task_id)
        elif choice == '4':
            task_id = int(input("Enter task ID to mark as completed: "))
            mark_task_completed(task_id)
        elif choice == '5':
            pass  # Implement search later
        elif choice == '6':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
