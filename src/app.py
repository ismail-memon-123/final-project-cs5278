import tkinter as tk
from tkinter import messagebox, simpledialog
from task import TaskFactory
from interpreter import Interpreter, CommandParser, FlexibleTaskParser, FixedTaskParser
from scheduler import ScheduleCommand, Scheduler, AddTaskCommand
from task import TaskFactory
from threading import Thread
from strategy import SchedulingStrategy, EarliestSlotStrategy, SingleTaskPerDayAndStartAt9Strategy

# This class is the GUI version of the command line app, it uses the same code but with more GUI connected elements.

class SchedulerApp:
    # Initiation of variables.
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")
        self.strategy = None
        self.scheduler = None
        self.flexible_tasks = []
        self.fixed_tasks = []
        self.schedules = []
        self.current_schedule_index = 0

        self.main_frame = None
        self.create_strategy_selection_page()
    
    # First page, we choose the strategy, using the strategy pattern a selected strategy is then passed on to
    # the Scheduler class using the set_strategy method.
    def create_strategy_selection_page(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        tk.Label(self.main_frame, text="Choose Scheduling Strategy", font=("Arial", 16)).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Earliest Slot Strategy",
            command=lambda: self.set_strategy(EarliestSlotStrategy),
            width=30
        ).pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Single Task Per Day Strategy Start At 9",
            command=lambda: self.set_strategy(SingleTaskPerDayAndStartAt9Strategy),
            width=30
        ).pack(pady=5)

    # Receives a strategy and sets self.scheduler to a Scheduler with that provided strategy.
    def set_strategy(self, strategy_cls):
        self.strategy = strategy_cls()
        self.scheduler = Scheduler(self.strategy)
        
        self.create_task_input_page()

    # This allows for the user to enter tasks. Depending on the button pressed, the appropriate parser (fixed,
    # flexible, or command) is used and passed on to the interpreter method.
    def create_task_input_page(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        tk.Label(self.main_frame, text="Add Tasks", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Fixed Tasks").grid(row=1, column=0, padx=10)
        tk.Label(self.main_frame, text="Flexible Tasks").grid(row=1, column=1, padx=10)

        self.fixed_task_listbox = tk.Listbox(self.main_frame, height=10, width=30)
        self.fixed_task_listbox.grid(row=2, column=0, padx=10, pady=10)

        self.flexible_task_listbox = tk.Listbox(self.main_frame, height=10, width=30)
        self.flexible_task_listbox.grid(row=2, column=1, padx=10, pady=10)

        self.task_name_entry = tk.Entry(self.main_frame, width=20)
        self.task_name_entry.grid(row=3, column=0, columnspan=2, pady=5)
        self.task_name_entry.insert(0, "Task Name")

        self.task_duration_entry = tk.Entry(self.main_frame, width=20)
        self.task_duration_entry.grid(row=4, column=0, columnspan=2, pady=5)
        self.task_duration_entry.insert(0, "Duration (hours)")

        self.task_days_entry = tk.Entry(self.main_frame, width=20)
        self.task_days_entry.grid(row=5, column=0, columnspan=2, pady=5)
        self.task_days_entry.insert(0, "Days (e.g., M, T, W, R, F, S, U)")

        self.task_start_time_entry = tk.Entry(self.main_frame, width=20)
        self.task_start_time_entry.grid(row=6, column=0, columnspan=2, pady=5)
        self.task_start_time_entry.insert(0, "Start Time (only for fixed tasks)")

        tk.Button(
            self.main_frame, text="Add Fixed Task", command=lambda:self.interpreter(FixedTaskParser, "fixed")
        ).grid(row=7, column=0, pady=10)

        tk.Button(
            self.main_frame, text="Add Flexible Task", command=lambda:self.interpreter(FlexibleTaskParser, "flexible")
        ).grid(row=7, column=1, pady=10)

        tk.Button(
            self.main_frame, text="Calculate Schedule", command=lambda:self.interpreter(CommandParser, "command")
        ).grid(row=8, column=0, columnspan=2, pady=20)


    # This method takes the class of type Interpreter and then builds an input string for the interpreter to
    # interpret. For the task we use the factory method to create the task. And then the command 
    # pattern to add it (as of now we have adding but this allows for further extensibilty later). The only
    # command here is calculate_schedule so we do that if that button pressed.
    def interpreter(self, interpreter_stub, prepend):
        interpreter_created = interpreter_stub()
        name = self.task_name_entry.get()
        duration = self.task_duration_entry.get()
        days = self.task_days_entry.get()
        start_time = self.task_start_time_entry.get()
        combined = prepend + " " + name + " " + duration + " " + days + " " + start_time
        task_type, name, duration, start_time, days_of_week = interpreter_created.parse(combined)
        if prepend != "command":
            task = TaskFactory.create_task(task_type, name, duration, days_of_week, start_time)
            add = AddTaskCommand(self.scheduler, task)
            add.execute()
            if type(interpreter_created) is FixedTaskParser:
                self.fixed_task_listbox.insert(self.fixed_task_listbox.size(), combined)
            else:
                self.flexible_task_listbox.insert(self.flexible_task_listbox.size(), combined)
        # only one type of command here
        else:
            self.calculate_schedule()

    # This method places fixed tasks and generates the flexible schedules and goes to the page to display schedules.
    def calculate_schedule(self):
        self.scheduler.generate_fixed_schedule()
        self.schedules = self.scheduler.generate_flexible_schedules()
        print(self.schedules)
        if not self.schedules:
            messagebox.showinfo("No Schedules", "No possible schedules were found or only fixed tasks provided.")
        else:
            self.current_schedule_index = 0
            self.show_schedule_page()

    # This metho builds the schedule page with a text box where the schedule can be printed.
    def show_schedule_page(self):
        self.clear_frame()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        tk.Label(self.main_frame, text=f"Schedule {self.current_schedule_index + 1}", font=("Arial", 16)).pack(pady=10)

        self.schedule_text = tk.Text(self.main_frame, height=20, width=50)
        self.schedule_text.pack(pady=10)
        self.display_schedule()

        tk.Button(
            self.main_frame,
            text="Next Schedule",
            command=self.next_schedule,
        ).pack(pady=10)
        
        tk.Button(
            self.main_frame,
            text="Save Schedule",
            command=self.save_schedule,
        ).pack(pady=10)

    # This method actually displays that schedule by inserting in the box the output of the printing of the 
    # schedule at the current index.
    def display_schedule(self):
        self.schedule_text.delete(1.0, tk.END)
        if len(self.schedules) == 0:
            self.schedule_text.insert(self.scheduler.week.print_day_tasks())
        else:
            schedule = self.schedules[self.current_schedule_index]
            string = schedule.week.print_day_tasks()
            self.schedule_text.insert('1.0', string)

    # This method increments the index and displays the next schedule.
    def next_schedule(self):
        self.current_schedule_index += 1
        if self.current_schedule_index >= len(self.schedules):
            messagebox.showinfo("End of Schedules", "No more schedules available.")
        else:
            self.display_schedule()

    # This method saves the schedule but first asks the name of the file to save to.
    def save_schedule(self):
        answer = tk.simpledialog.askstring("Save file dialog", "What filename would you like to save to")
        with open(answer, 'w') as file:
            schedule = self.schedules[self.current_schedule_index]
            file.write(schedule.week.print_day_tasks())
        print("Saved schedule successfully")
    
    # This method clears the screen.
    def clear_frame(self):
        if self.main_frame:
            self.main_frame.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
