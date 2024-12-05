# This class manages the free time of each of the schedules.
class Week:

    # Initiation. the week has an array of size 24*7 to schedule each hour of the week. Also takes in a strategy
    # which dictates how it will place tasks.
    def __init__(self, strategy):
                                   #0 am  1 am 2 am
                                   # M T W R F S U
        self.twentyfour_hr_sched = [None] * 24 * 7
        self.strategy = strategy

    # Depending on the strategy, this method returns a list of ints (times) that the task can be scheduled.
    def get_available_slots(self, duration):
        return self.strategy.get_available_slots(self.twentyfour_hr_sched, duration)
    
    # place_task will take a task and place it at a start hour and block the time needed that its duration requires.
    def place_task(self, task, start_hour):
        for hour in range(start_hour, start_hour + task.duration):
            self.twentyfour_hr_sched[hour] = task
            print(task.name)
            print("placed at " + str(hour))

    # Remove task removes a task from its start hour to how long its duration is.
    def remove_task(self, task, start_hour):
        for hour in range(start_hour, start_hour + task.duration):
            self.twentyfour_hr_sched[hour] = None
    
    # This method prints out the week schedule in a neat way to save or display on screen.
    def print_day_tasks(self):
        string = ""
        for j in range(7):
            if (j == 0):
                string += "Monday:\n"
            if (j == 1):
                string += "Tuesday:\n"
            if (j == 2):
                string += "Wednesday:\n"
            if (j == 3):
                string += "Thursday:\n"
            if (j == 4):
                string += "Friday:\n"
            if (j == 5):
                string += "Saturday:\n"
            if (j == 6):
                string += "Sunday:\n"
            for i in range(24):
                if (i < 12):
                    if self.twentyfour_hr_sched[j*24 + i] is not None:
                        string += "\t" + str(i) + "-" + (str(i+1)) + " am: " + self.twentyfour_hr_sched[j*24 + i].name + "\n"
                    else:
                        string += "\t" + str(i) + "-" + (str(i+1)) + " am: " + "\n"
                else:
                    if self.twentyfour_hr_sched[j*24 + i] is not None:
                        string += "\t" + str(i-12) + "-" + (str(i-11)) + " pm: " + self.twentyfour_hr_sched[j*24 + i].name + "\n"
                    else:
                        string += "\t" + str(i-12) + "-" + (str(i-11)) + " pm: " + "\n"
        return string