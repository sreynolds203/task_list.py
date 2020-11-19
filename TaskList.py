import psycopg2
from tkinter import Listbox, StringVar, Toplevel, messagebox, ttk
from tkinter.ttk import Combobox, Label, Entry, Button
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
from datetime import datetime

# Creates a database connection and a cursor
# for use throughout the application
conn = psycopg2.connect(host='localhost',
                        port='5432',
                        user='pi',
                        password='server',
                        database='Task_list')

cur = conn.cursor()


# A topleve window that allows the user to add
# a new task to the listbox on the main window.
# The information is also saved to the database.
def add_task():
    # Creates a topleve window and sets the size and color
    at = Toplevel(root)
    at.title('New Task')
    at.geometry('550x320')
    at.configure(bg='gray20')

    # Creates a style that can be used on the buttons
    # for added colors and theme components
    style = ttk.Style()
    style.configure('TButton',
                    foreground='orange')

    # Label and entry for the task
    at_name = Label(at,
                    text='Task Name:')
    at_name.grid(column=0,
                 row=0,
                 padx=10,
                 pady=10,
                 sticky='w')
    at_name.configure(foreground='orange',
                      background='gray20')

    at_name_entry = Entry(at)
    at_name_entry.grid(column=0,
                       row=1,
                       padx=10,
                       pady=10,
                       columnspan=3,
                       sticky='ew')

    # Label and calendar dropdown for task due date
    at_due_date = Label(at,
                        text='Due Date:')
    at_due_date.grid(column=0,
                     row=2,
                     padx=10,
                     pady=10,
                     sticky='w')
    at_due_date.configure(foreground='orange',
                          background='gray20')

    start_date = DateEntry(at)
    start_date.grid(column=0,
                    row=3,
                    padx=10,
                    pady=10,
                    sticky='w')
    start_date._top_cal.overrideredirect(False)
    start_date.configure(foreground='orange',
                         background='gray20')

    # Label and dropdown for the user to select a priority
    # level of the task
    at_priority_label = Label(at,
                              text='Priority Level:')
    at_priority_label.grid(column=0,
                           row=4,
                           padx=10,
                           pady=10,
                           sticky='w')
    at_priority_label.configure(foreground='orange',
                                background='gray20')

    p = StringVar()
    p_level = Combobox(at,
                       width=4,
                       textvariable=p)
    p_level.grid(column=0,
                 row=5,
                 padx=10,
                 pady=10,
                 sticky='w')
    p_level['values'] = ('0', '1', '2', '3', '4', '5')
    p_level.current(0)

    # Nested function to save the task information for the add
    # task window to the database. Also updates the listbox
    # located on the main window.
    def save_task():
        task_name = str(at_name_entry.get())
        sdate = start_date.get()
        convert_date = datetime.strptime(sdate, "%m/%d/%y").date()
        prio = int(p_level.get())
        comp = False
        if len(task_name) == 0:
            messagebox.showinfo('Empty Entry', 'Task is blank')
        else:
            save_statement = '''
                    INSERT INTO
                        Tasks (task_name, due_date, p_level, comp_status)
                    VALUES
                        (%s, %s, %s, %s)
                    '''
            save_vals = (task_name, convert_date, prio, comp)
            cur.execute(save_statement, save_vals)
            conn.commit()
        update_list()
        at.destroy()

    # Save and cancel buttons to save the task or to close the
    # toplevel window without submitting the information to the
    # database.
    save_button = Button(at, text='Save',
                         command=save_task,
                         style='TButton')
    save_button.grid(column=2,
                     row=6,
                     padx=10,
                     pady=10,
                     sticky='e')

    cancel_button = Button(at, text='Cancel',
                           command=at.destroy,
                           style='TButton')
    cancel_button.grid(column=3,
                       row=6,
                       padx=10,
                       pady=10,
                       sticky='w')

    # Adjusts the weight of the column in the toplevel window
    at.columnconfigure(0, weight=1)
    at.mainloop()


# Function to clear the listbox contents
def empty_list():
    _list.delete(0, 'end')


# Function to delete a task from the database and update the
# listbox contents
def del_task():
    val = _list.get(_list.curselection())
    val_term = val.index('--')
    strip_line = val[:val_term]
    strip_line = strip_line.rstrip()
    del_statement = '''
        DELETE FROM
            Tasks
        WHERE
            task_name = %s;
        '''
    vals = (strip_line,)
    cur.execute(del_statement, vals)
    conn.commit()
    update_list()


# Function to update a task as completed in database and
# update the listbox with incomplete tasks
def comp_task():
    content = str(_list.selection_get())
    term = content.index('--')
    strip_cont = content[:term]
    strip_cont = strip_cont.rstrip()
    statement = '''
        UPDATE
            Tasks
        SET
            comp_status = TRUE
        WHERE
            task_name = %s;
        '''
    cur.execute(statement, (strip_cont,))
    conn.commit()
    update_list()


# Function that updates the listbox and color codes the
# tasks based on the priority level:
# 0 = blue, 1 = purple, 2 = green, 3 = yellow,
# 4 = orange, 5 = red
def update_list():
    empty_list()
    s_query = '''
        SELECT
            task_name, due_date, p_level
        FROM
            Tasks
        WHERE
            comp_status = false
        ORDER BY
            due_date, p_level
        '''
    cur.execute(s_query)
    results = cur.fetchall()
    for i in results:
        task_name = i[0]
        convert_date = str(i[1])
        prio = str(i[2])
        _list.insert('end',
                     f"{task_name}--Due: {convert_date}--Priority: {prio}")
    count = 0
    for line in _list.get(0, 'end'):
        str_size = len(line)
        p_index = str_size - 1
        if line[p_index:] == '1':
            _list.itemconfigure(count, {'fg': 'purple2'})
        elif line[p_index:] == '2':
            _list.itemconfigure(count, {'fg': 'green'})
        elif line[p_index:] == '3':
            _list.itemconfigure(count, {'fg': 'yellow'})
        elif line[p_index:] == '4':
            _list.itemconfigure(count, {'fg': 'orange'})
        elif line[p_index:] == '5':
            _list.itemconfigure(count, {'fg': 'tomato'})
        else:
            _list.itemconfigure(count, {'fg': 'royalblue3'})
        count += 1


# Main window and the components of the window. The theme, title, size,
# and background color are set.
root = ThemedTk(theme='equilux')
root.title('Task List')
root.geometry('550x500')
root.configure(bg='gray20')

# Creates a style for use in the buttons of the main page.
style = ttk.Style()
style.configure('TButton',
                foreground='orange')

# Listbox to view the tasks
_list = Listbox(root,
                height=10,
                bg='gray12')
_list.grid(column=0,
           row=0,
           padx=2,
           pady=2,
           columnspan=6,
           sticky='nsew')
update_list()

# Buttons for the main page.
new_button = Button(root,
                    text='New',
                    command=add_task,
                    style='TButton')
new_button.grid(column=1,
                row=1,
                padx=2,
                pady=2,
                sticky='w')

delete_button = Button(root,
                       text='Delete',
                       command=del_task,
                       style='TButton')
delete_button.grid(column=2,
                   row=1,
                   padx=2,
                   pady=2,
                   sticky='w')

comp_button = Button(root,
                     text='Completed',
                     command=comp_task,
                     style='TButton')
comp_button.grid(column=3,
                 row=1,
                 padx=2,
                 pady=2,
                 sticky='w')

# Adjusts the size of specific rows and columns
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()

cur.close()
