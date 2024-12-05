# The class Task is an interface that both FixedTask and FlexibleTask implement.
class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration  # in hours

# Fixed Tasks is provided days of week and a start time, along with name and duration.
class FixedTask(Task):
    def __init__(self, name, duration, days_of_week, start_time):
        super().__init__(name, duration)
        self.start_time = start_time
        self.days_of_week = days_of_week
        print("HERE1")

# Flexible task only needs name and duration, as it can be flexed into any day if the strategy allows.
class FlexibleTask(Task):
    def __init__(self, name, duration):
        super().__init__(name, duration)
        print("HERE2")

# This class is the implementation of the factoy method pattern. Provided these parameters, the class will
# return a FixedTask or FlexibleTask depending on the type, as the output of the create_task method.
class TaskFactory:
    @staticmethod
    def create_task(task_type, name, duration, days_of_week, start_time=None):
        if task_type == "fixed":
            if start_time is None:
                raise ValueError("Fixed tasks require a start time.")
            return FixedTask(name, duration, days_of_week, start_time)
        elif task_type == "flexible":
            return FlexibleTask(name, duration)
        else:
            raise ValueError("Unknown task type.")
