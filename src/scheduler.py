from datetime import timedelta
from task import Task, FixedTask, FlexibleTask
from week import Week
from copy import deepcopy

# This is the use of the command pattern, each class that implements it needs an execute method.
class ScheduleCommand:
    def execute(self):
        raise NotImplementedError("You should implement this method.")

# Currently we only have the AddTaskCommand, it adds a task to the schedule using its add_task method.
class AddTaskCommand(ScheduleCommand):
    def __init__(self, schedule, task):
        self.schedule = schedule
        self.task = task

    def execute(self):
        self.schedule.add_task(self.task)

    def undo(self):
        self.schedule.remove_task(self.task)

# The scheduler class holds each potential schedule.
class Scheduler:
    # Init method takes in a strategy to initiate the Week object with.
    def __init__(self, strategy):
        self.tasks = []
        self.week = Week(strategy)

    # add_task adds a task to the tasks array.
    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task added: {task.name}")

    # removed removes a task from the tasks array
    def remove_task(self, task):
        self.tasks.remove(task)
        print(f"Task removed: {task.name}")
    
    # This method executes the inputted command.
    def execute_command(self, command):
        command.execute()
    
    # This method places the fixed tasks where they are supposed to be in the week object.
    def generate_fixed_schedule(self):
        #main logic of how this will work
        # first we will assign all the fixed tasks.
        for i in self.tasks:
            if isinstance(i, FixedTask):
                for j in range(7):
                    if i.days_of_week[j]:
                        self.week.place_task(i, j*24 + i.start_time)

    # This method generates the possible differnet flexible schedule combinations. It takes a task and places
    # it and then backtracks the remianing tasks.
    def backtrack(self, remaining_tasks, current_schedule, results):
        if not remaining_tasks:  # All tasks placed
            results.append(deepcopy(current_schedule))
            return

        task = remaining_tasks[0]
        available_slots = current_schedule.week.get_available_slots(task.duration)
        print(available_slots)

        for start_hour in available_slots:
            # Create a new schedule to try this placement
            new_schedule = deepcopy(current_schedule)
            new_schedule.week.place_task(task, start_hour)
            self.backtrack(remaining_tasks[1:], new_schedule, results)
    
    # This method generates the flexible schedules by using the backtrack method. It returns a list of 
    # objects of type Scheduler that can be exmained and printed as they have contained the different schedules.
    def generate_flexible_schedules(self):
        flex_tasks = []
        results = []
        for i in self.tasks:
            if isinstance(i, FlexibleTask):
                flex_tasks.append(i)

        self.backtrack(flex_tasks, deepcopy(self), results)
        return results


