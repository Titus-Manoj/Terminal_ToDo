import sqlite3

connection = sqlite3.connect("ToDo.db")
#print(connection.total_changes)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    task_status TEXT NOT NULL DEFAULT "Pending"
                );""")

def add_task():
    task_name = input("Enter task: ")
    #Get count till now and add next value
    #cursor.execute("SELECT COALESCE(MAX(ID), 0) AS total_entries FROM tasks")
    #Max(ID) gives value null when empty table, so COALESCE(MAX(ID) gives 0 when null
    cursor.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
    #cursor.execute("INSERT INTO tasks (task_name) VALUES (:jack)", {'jack': "Settle Bills", })
    #cursor.execute("INSERT INTO tasks (task_name, task_status) VALUES (:jack, :status)", {'jack': "Schedule driving test", 'status': "Completed"})
    connection.commit()
    print(f"Task '{task_name}' added successfully!")

def edit_task():
    view_all_tasks()
    input_str = input("Enter task id that is to be edited and new task name: ")
    num_str = ""
    for char in input_str:
        if char.isdigit():
            num_str += char  # Build the number part
        else:
            break  # Stop when non-digit is encountered
    num = int(num_str)  # Convert number part to an integer
    task_name = input_str[len(num_str):].strip()
    #Split the number and task name, if id not present give error and to try again
    cursor.execute("UPDATE tasks SET task_name = ? WHERE id = ?", (task_name, num))
    connection.commit()
    view_all_tasks()

def view_all_tasks():
    print("\n")
    cursor.execute("SELECT id || '. ' || task_name || ' - ' || task_status AS formatted_task FROM tasks ORDER BY id")
    tasks = cursor.fetchall()
    if not tasks:
        print("No Tasks Present")
    for row in tasks:
        print(row[0])

def delete_task():
    view_all_tasks()
    task_num = input("Enter task number that is to be deleted: ")
    cursor.execute("DELETE FROM tasks WHERE id = ?",(task_num,))
    cursor.execute("""
        UPDATE tasks
        SET id = id - 1
        WHERE id > ?;
    """, (task_num,))
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'tasks';")
    connection.commit()
    view_all_tasks()

def mark_as_done():
    view_all_tasks()
    task_id = input("Input task number to be maked as Done: ")
    cursor.execute("UPDATE tasks SET task_status = 'Completed' WHERE id = ?", (task_id))
    connection.commit()

def mark_as_undone():
    view_all_tasks()
    task_id = input("Input task number to be maked as Work Pending: ")
    cursor.execute("UPDATE tasks SET task_status = 'Pending' WHERE id = ?", (task_id))
    connection.commit()

def view_tasks_by_status():
    cmd = input("View tasks completed(c) or pending(p): ")
    if cmd.lower() == 'c':
        cursor.execute("SELECT id || '. ' || task_name || ' - ' || task_status AS formatted_task FROM tasks WHERE task_status = 'Completed' ORDER BY id")
    elif cmd.lower() == 'p':
        cursor.execute("SELECT id || '. ' || task_name || ' - ' || task_status AS formatted_task FROM tasks WHERE task_status = 'Pending' ORDER BY id")
    else:
        print("Input to be in format: c - completed OR p - pending. Try Again Later")
        return
    tasks = cursor.fetchall()
    if not tasks:
        print("No Tasks Present")
    for row in tasks:
        print(row[0])

def main():
    while True:
        print("\n Choose from following options:")
        #add, view, edit, delete, and mark as completed
        print("1. Add ToDo")
        print("2. Edit ToDo")
        print("3. Delete ToDo")
        print("4. Mark as Completed")
        print("5. Mark as Pending")
        print("6. View all Tasks")
        print("7. View Tasks by Status")
        print("8. Exit \n")
        choice = input("Enter your choice: \n")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            edit_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            mark_as_done()
        elif choice == "5":
            mark_as_undone()
        elif choice == "6":
            view_all_tasks()
        elif choice == "7":
            view_tasks_by_status()
        elif choice == "8":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

connection.close()