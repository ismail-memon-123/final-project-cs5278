from abc import ABC, abstractmethod

# The interpreter class has the parse method which all must implement. The parse method returns the parameters that
# were parsed from user input.
class Interpreter(ABC):
    @abstractmethod
    def parse(self, input_str):
        raise NotImplementedError

# Command parser will return the string 'command' and the name of the command
class CommandParser(Interpreter):
    def parse(self, input_str):
        task_type = "command"
        name = input_str
        return task_type, name, None, None, None
        

# Flexible task parser will return the name and duration, and 'flexible' as task_type
class FlexibleTaskParser(Interpreter):
    def parse(self, input_str): 
        # Expected format: "fixed|flexible TaskName 1 Day(s) [14]" for fixed tasks
        parts = input_str.split()
        task_type = "flexible"
        name = parts[1]
        duration = int(parts[2])
        return task_type, name, duration, None, None

# FixedTaskParser will return 'fixed' as task_type, name, duration, days_of_week, and start_time. Start_time is
# hour of day the task starts, so 9 for 9 AM. Days of week is an array of 7 for each of the days and true if
# the task is for that day and false if not. So if some fixed task is MTWRF then the days_of_week will be
# [True, True, True, True, True, False, False].
class FixedTaskParser(Interpreter):
    def parse(self, input_str):
        # Expected format: "fixed|flexible TaskName 1 Day(s) [14]" for fixed tasks
        parts = input_str.split()
        task_type = "fixed"
        name = parts[1]
        duration = int(parts[2])       
        days = parts[3]
        start_time = int(parts[4]) if task_type == "fixed" else None
        days_of_week = []
        # True for what day of week has it so if MTF, it will be [true, true, false, false, true, false, false]
        if ('M' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)
        if ('T' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)
        if ('W' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)
        if ('R' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)
        if ('F' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)
        if ('S' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)
        if ('U' in days):
            days_of_week.append(True)
        else:
            days_of_week.append(False)

        return task_type, name, duration, start_time, days_of_week
