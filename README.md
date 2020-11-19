# task_list.py

This project is a task manager that I created for my own use using python, postgresql and tkinter.
The idea for this project came from the lack of finding a task manager that met my needs and 
did not include unnecessary features that slow the application down. 
Each task contains a text entry of the task itself, a due date, adn a priority level ranging from 0-5. 
The tasks are colored based on the level of priority:
  0 = blue
  1 = purple
  2 = green
  3 = yellow
  4 = orange
  5 = red
  
 When a task is added, the task information is added to the database and the main screen refreshes
 the Listbox from the database. 
 When a task is completed, the complete button updates the database and marks the task as complete. 
 The task remains in the database but does not show in the list.
 When task is deleted, it is removed from the list as well as the database. 
