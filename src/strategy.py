from abc import ABC, abstractmethod

# This class implements the Strategy pattern, and each strategy must implement the get_available_slots method
# so that we can have proper behavior.
class SchedulingStrategy(ABC):
    @abstractmethod
    def get_available_slots(self, twentyfour_hr_sched, task_duration):
        raise NotImplementedError

# The earliest slot strategy sequentially goes through the schedule and starts off with the earliest slots
# available, but it will go through all possibilities.
class EarliestSlotStrategy(SchedulingStrategy):
    def __init__(self):
        pass
    
    # Checks if in the schedule and start hour an opening is available of length duration.
    def is_slot_free(self, start_hour, twentyfour_hr_sched, duration):
        if (start_hour + duration) > len(twentyfour_hr_sched):
            return False
        print(str(duration))
        print(str(start_hour))
        return all(twentyfour_hr_sched[hour] is None for hour in range(start_hour, start_hour + duration))

    def get_available_slots(self, twentyfour_hr_sched, duration):
        return_list = []
        for i in range(len(twentyfour_hr_sched)):
            if self.is_slot_free(i, twentyfour_hr_sched, duration):
                return_list.append(i)
        return return_list


# SingleTaskPerDayAndStartAt9Strategy only allows one flexible task per day and it starts at 9, and if one fixed
# task is already present per day, that day won't get a fixed task.
class SingleTaskPerDayAndStartAt9Strategy(SchedulingStrategy):
    def __init__(self):
        pass
    
    # Checks if in the schedule and start hour an opening is available of length duration.
    def is_slot_free(self, start_hour, twentyfour_hr_sched, duration):
        if (start_hour + duration) > len(twentyfour_hr_sched):
            return False
        print(str(duration))
        print(str(start_hour))
        return all(twentyfour_hr_sched[hour] is None for hour in range(start_hour, start_hour + duration))

    def get_available_slots(self, twentyfour_hr_sched, duration):
        #Only one task per day allowed so we need something that is free a full day hours and then we can schedule it anytime
        return_list = []
        for day in range(7):  # Loop through 7 days
            # if whole day is free
            if self.is_slot_free(day*24, twentyfour_hr_sched, 24):
                day_start = day * 24  # Start hour of the day
                return_list.append(day_start+9)
        return return_list
