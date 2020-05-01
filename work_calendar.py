from datetime import datetime
from models.Node_BST import BST
from models.FileRW import FileRW
from models.invokers import Invokers


def event_input():
    while True:
        print("Type the event's start time. Format hh:mm, like 06:20 or 12:05.")
        start_time = input("> ").strip()
        try:
            datetime.strptime(start_time, '%H:%M')
        except ValueError:
            print("Incorrect time format, should be hh:mm.")
        else:
            break

    while True:
        print("Type the event's duration in minutes. Format mm, like 05 or 90.")
        duration_minutes = input("> ").strip()
        try:
            int(duration_minutes)
        except ValueError:
            print("Please enter a number for number of minutes")
        else:
            break

    print("Type the title of the event. Recommended format: Event name or Event Name.")
    event_name = input("> ").strip()

    return start_time, duration_minutes, event_name


print("Welcome to the Work Calendar")

bst = BST()
file_rw = FileRW(bst)
invoke = Invokers()

file_rw.read_insert_to_bst()
bst.in_order_event_printer()

tasks = ("show", "add", "rem", "free", "esc")

while True:
    print("What do you want to do next?")
    print(f"Enter '{tasks[0]}' to show work calendar.")
    print(f"Enter '{tasks[1]}' to add event or task to the calendar.")
    print(f"Enter '{tasks[2]}' to remove event or task from the calendar.")
    print(f"Enter '{tasks[3]}' to show free-time intervals.")
    print(f"Enter '{tasks[-1]}' to close the program.")
    print(">", end=" ")
    task = input()

    try:
        if not getattr(invoke, task)(bst, file_rw, event_input):
            break
    except (AttributeError, ValueError):
        print("You entered an invalid task, please chose one of the followings:")
        print(", ".join(tasks))
        print("")
