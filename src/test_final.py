from interpreter import Interpreter, CommandParser, FlexibleTaskParser, FixedTaskParser
from scheduler import ScheduleCommand, Scheduler, AddTaskCommand
from task import TaskFactory, FixedTask, FlexibleTask
from strategy import SchedulingStrategy, EarliestSlotStrategy, SingleTaskPerDayAndStartAt9Strategy

import pytest

# Test class.
class TestFinalProject():
    @staticmethod
    def test_initial():
        pass
    
    # Checks if the interpreter can properly parse a fixed task.
    @staticmethod
    def test_interpreter_fixed_parse():
        interpreter = FixedTaskParser()
        task_type, name, duration, start_time, days_of_week = interpreter.parse("fixed Work 9 MTWRF 9")
        assert task_type == "fixed"
        assert name == "Work"
        assert duration == 9
        assert start_time == 9
        assert days_of_week == [True, True, True, True, True, False, False]
    
    # Checks if the interpreter can properly parse a flexible task.
    @staticmethod
    def test_interpreter_flexbile_parse():
        interpreter = FlexibleTaskParser()
        task_type, name, duration, start_time, days_of_week = interpreter.parse("flexible laundry 4")
        assert task_type == "flexible"
        assert name == "laundry"
        assert duration == 4
        assert start_time is None
        assert days_of_week is None
    
    # Checks if the interpreter can properly parse a variety of commands.
    @staticmethod
    def test_interpreter_command_parse():
        interpreter = CommandParser()
        task_type, name, duration, start_time, days_of_week = interpreter.parse("calculate")
        assert task_type == "command"
        assert name == "calculate"
        assert duration is None
        assert start_time is None
        assert days_of_week is None
        
        task_type, name, duration, start_time, days_of_week = interpreter.parse("next schedule")
        assert task_type == "command"
        assert name == "next schedule"
        assert duration is None
        assert start_time is None
        assert days_of_week is None
        
        task_type, name, duration, start_time, days_of_week = interpreter.parse("save")
        assert task_type == "command"
        assert name == "save"
        assert duration is None
        assert start_time is None
        assert days_of_week is None
        
        task_type, name, duration, start_time, days_of_week = interpreter.parse("invalid bogus")
        assert task_type == "command"
        assert name == "invalid bogus"
        assert duration is None
        assert start_time is None
        assert days_of_week is None
    
    # Checks if the the task factory can create a fixed and flexible task properly.
    @staticmethod
    def test_task_creations():
        task = TaskFactory.create_task("fixed", "Work", 9, "MTWR", 8)
        assert type(task) == FixedTask
        assert task.name == "Work"
        assert task.duration == 9
        assert task.start_time == 8
        assert task.days_of_week == "MTWR"
        
        task = TaskFactory.create_task("flexible", "Laundry", 6, None)
        assert type(task) == FlexibleTask
        assert task.name == "Laundry"
        assert task.duration == 6
    
    
    # Checks if the EarliestSlotStrategy has a get_available_slots methods that correctly fills the first available
    # slots before proceeding to other slots.
    @staticmethod
    def test_strategy_EarliestSlotStrategy():
        strategy = EarliestSlotStrategy()
        twentyfour_hr_sched = [None] * 24 * 7
        twentyfour_hr_sched[0] = 1
        twentyfour_hr_sched[1] = 1
        twentyfour_hr_sched[6] = 1
        list_slots = strategy.get_available_slots(twentyfour_hr_sched, 3)
        # assert that this is earliest first bec the first gap should be filled and that should be the return answer
        assert list_slots[0] == 2
        assert len(list_slots) == 161

    
    # Checks if the SingleTaskPerDayAndStartAt9Strategy has a get_available_slots methods that correctly fills the first available
    # slots for flexible tasks only if there isnt something already in the day 
    @staticmethod
    def test_strategy_SingleTaskPerDayAndStartAt9Strategy():
        strategy = SingleTaskPerDayAndStartAt9Strategy()
        twentyfour_hr_sched = [None] * 24 * 7
        twentyfour_hr_sched[0] = 1
        twentyfour_hr_sched[9] = 1
        twentyfour_hr_sched[33] = 1
        twentyfour_hr_sched[81] = 1
        twentyfour_hr_sched[153] = 1
        list_slots = strategy.get_available_slots(twentyfour_hr_sched, 3)
        # assert that this is single task at 9 because it should be only available for 3 days, WFS at 9 am so that would be 57, 105, 129
        assert list_slots[0] == 57
        assert list_slots[1] == 105
        assert list_slots[2] == 129
        assert len(list_slots) == 3
    
    # Checks if the AddTaskCommand properly inserts a new task in the schedule.
    @staticmethod
    def test_scheduler_AddTask():
        schedule = Scheduler(SingleTaskPerDayAndStartAt9Strategy())
        task = TaskFactory.create_task("fixed", "Work", 9, "MTWRF", start_time=9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        assert len(schedule.tasks) == 1
        assert schedule.tasks[0].name == "Work"
    
    
    # This method checks whether the generate_fixed_schedule method properly places the fixed tasks in the correct
    # indices in the week's twentyfour_hr_sched array. Using the SingleTaskPerDayAndStartAt9Strategy
    @staticmethod
    def test_scheduler_generate_fixed_SingleTaskPerDayAndStartAt9Strategy():
        schedule = Scheduler(SingleTaskPerDayAndStartAt9Strategy())
        task = TaskFactory.create_task("fixed", "Work", 4, [True, True, True, True, False, False, False], 9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        task2 = TaskFactory.create_task("flexible", "Laundry", 4, None)
        add2 = AddTaskCommand(schedule, task2)
        add2.execute()
        schedule.generate_fixed_schedule()
        assert schedule.week.twentyfour_hr_sched is not [None]*24*7
        print(str(schedule.week.twentyfour_hr_sched))
        # four days we have work so the four days should be recorded in fixed schedule
        assert schedule.week.twentyfour_hr_sched[9:13] == [task, task, task, task]
        assert schedule.week.twentyfour_hr_sched[33:37] == [task, task, task, task]
        assert schedule.week.twentyfour_hr_sched[57:61] == [task, task, task, task]
        assert schedule.week.twentyfour_hr_sched[81:85] == [task, task, task, task]
        print(str(schedule.week.twentyfour_hr_sched))

    # This method checks whether the generate_fixed_schedule method properly places the fixed tasks in the correct
    # indices in the week's twentyfour_hr_sched array. Using the EarliestSlotStrategy    
    @staticmethod
    def test_scheduler_generate_fixed_EarliestSlotStrategy():
        # behavior should be the same regardless of strategy since its just fixed
        schedule = Scheduler(EarliestSlotStrategy())
        task = TaskFactory.create_task("fixed", "Work", 4, [True, True, True, True, False, False, False], 9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        task2 = TaskFactory.create_task("flexible", "Laundry", 4, None)
        add2 = AddTaskCommand(schedule, task2)
        add2.execute()
        schedule.generate_fixed_schedule()
        assert schedule.week.twentyfour_hr_sched is not [None]*24*7
        print(str(schedule.week.twentyfour_hr_sched))
        # four days we have work so the four days should be recorded in fixed schedule
        assert schedule.week.twentyfour_hr_sched[9:13] == [task, task, task, task]
        assert schedule.week.twentyfour_hr_sched[33:37] == [task, task, task, task]
        assert schedule.week.twentyfour_hr_sched[57:61] == [task, task, task, task]
        assert schedule.week.twentyfour_hr_sched[81:85] == [task, task, task, task]
        print(str(schedule.week.twentyfour_hr_sched))
    
    # This method checks whether the generate_flexible_schedules method properly places the flexilbe
    # tasks and creates all the possible combinations of schedules. Using the EarliestSlotStrategy
    @staticmethod
    def test_scheduler_generate_flexible_EarliestSlotStrategy():
        schedule = Scheduler(EarliestSlotStrategy())
        task = TaskFactory.create_task("fixed", "Work", 9, [True, True, True, True, True, True, True], 9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        task3 = TaskFactory.create_task("fixed", "Sleep", 9, [True, True, True, True, True, True, True], 0)
        add3 = AddTaskCommand(schedule, task3)
        add3.execute()
        task2 = TaskFactory.create_task("flexible", "Laundry", 6, None)
        add2 = AddTaskCommand(schedule, task2)
        add2.execute()
        schedule.generate_fixed_schedule()
        list_of_schedules = schedule.generate_flexible_schedules()
        # There should be 7 possible schedules as we can do laundry on any day between 6 pm - midnight
        assert len(list_of_schedules) == 7
        # Now test all the diff schedules
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[18]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[19]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[20]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[21]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[22]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[23]) is FlexibleTask
        assert list_of_schedules[0].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[18]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[19]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[20]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[21]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[22]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[23]) is FlexibleTask
        assert list_of_schedules[0].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[0].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[42]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[43]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[44]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[45]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[46]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[47]) is FlexibleTask
        assert list_of_schedules[1].week.twentyfour_hr_sched[18:24] == [None, None, None, None, None, None]
        assert list_of_schedules[1].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[1].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[1].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[1].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[1].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[2].week.twentyfour_hr_sched[66]) is FlexibleTask
        assert type(list_of_schedules[2].week.twentyfour_hr_sched[67]) is FlexibleTask
        assert type(list_of_schedules[2].week.twentyfour_hr_sched[68]) is FlexibleTask
        assert type(list_of_schedules[2].week.twentyfour_hr_sched[69]) is FlexibleTask
        assert type(list_of_schedules[2].week.twentyfour_hr_sched[70]) is FlexibleTask
        assert type(list_of_schedules[2].week.twentyfour_hr_sched[71]) is FlexibleTask
        assert list_of_schedules[2].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[2].week.twentyfour_hr_sched[18:24] == [None, None, None, None, None, None]
        assert list_of_schedules[2].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[2].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[2].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[2].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[3].week.twentyfour_hr_sched[90]) is FlexibleTask
        assert type(list_of_schedules[3].week.twentyfour_hr_sched[91]) is FlexibleTask
        assert type(list_of_schedules[3].week.twentyfour_hr_sched[92]) is FlexibleTask
        assert type(list_of_schedules[3].week.twentyfour_hr_sched[93]) is FlexibleTask
        assert type(list_of_schedules[3].week.twentyfour_hr_sched[94]) is FlexibleTask
        assert type(list_of_schedules[3].week.twentyfour_hr_sched[95]) is FlexibleTask
        assert list_of_schedules[3].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[3].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[3].week.twentyfour_hr_sched[18:24] == [None, None, None, None, None, None]
        assert list_of_schedules[3].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[3].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[3].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[4].week.twentyfour_hr_sched[114]) is FlexibleTask
        assert type(list_of_schedules[4].week.twentyfour_hr_sched[115]) is FlexibleTask
        assert type(list_of_schedules[4].week.twentyfour_hr_sched[116]) is FlexibleTask
        assert type(list_of_schedules[4].week.twentyfour_hr_sched[117]) is FlexibleTask
        assert type(list_of_schedules[4].week.twentyfour_hr_sched[118]) is FlexibleTask
        assert type(list_of_schedules[4].week.twentyfour_hr_sched[119]) is FlexibleTask
        assert list_of_schedules[4].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[4].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[4].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[4].week.twentyfour_hr_sched[18:24] == [None, None, None, None, None, None]
        assert list_of_schedules[4].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[4].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[5].week.twentyfour_hr_sched[138]) is FlexibleTask
        assert type(list_of_schedules[5].week.twentyfour_hr_sched[139]) is FlexibleTask
        assert type(list_of_schedules[5].week.twentyfour_hr_sched[140]) is FlexibleTask
        assert type(list_of_schedules[5].week.twentyfour_hr_sched[141]) is FlexibleTask
        assert type(list_of_schedules[5].week.twentyfour_hr_sched[142]) is FlexibleTask
        assert type(list_of_schedules[5].week.twentyfour_hr_sched[143]) is FlexibleTask
        assert list_of_schedules[5].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[5].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[5].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[5].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[5].week.twentyfour_hr_sched[18:24] == [None, None, None, None, None, None]
        assert list_of_schedules[5].week.twentyfour_hr_sched[162:168] == [None, None, None, None, None, None]
        
        assert type(list_of_schedules[6].week.twentyfour_hr_sched[162]) is FlexibleTask
        assert type(list_of_schedules[6].week.twentyfour_hr_sched[163]) is FlexibleTask
        assert type(list_of_schedules[6].week.twentyfour_hr_sched[164]) is FlexibleTask
        assert type(list_of_schedules[6].week.twentyfour_hr_sched[165]) is FlexibleTask
        assert type(list_of_schedules[6].week.twentyfour_hr_sched[166]) is FlexibleTask
        assert type(list_of_schedules[6].week.twentyfour_hr_sched[167]) is FlexibleTask
        assert list_of_schedules[6].week.twentyfour_hr_sched[42:48] == [None, None, None, None, None, None]
        assert list_of_schedules[6].week.twentyfour_hr_sched[66:72] == [None, None, None, None, None, None]
        assert list_of_schedules[6].week.twentyfour_hr_sched[90:96] == [None, None, None, None, None, None]
        assert list_of_schedules[6].week.twentyfour_hr_sched[114:120] == [None, None, None, None, None, None]
        assert list_of_schedules[6].week.twentyfour_hr_sched[138:144] == [None, None, None, None, None, None]
        assert list_of_schedules[6].week.twentyfour_hr_sched[18:24] == [None, None, None, None, None, None]

    # This method checks whether the generate_flexible_schedules method properly places the flexilbe
    # tasks and creates all the possible combinations of schedules. Using the SingleTaskPerDayAndStartAt9Strategy
    @staticmethod
    def test_scheduler_generate_flexible_SingleTaskPerDayAndStartAt9Strategy():
        schedule = Scheduler(SingleTaskPerDayAndStartAt9Strategy())
        task = TaskFactory.create_task("fixed", "Work", 9, [True, True, True, True, True, False, False], 9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        task2 = TaskFactory.create_task("flexible", "Laundry", 6, None)
        add2 = AddTaskCommand(schedule, task2)
        add2.execute()
        schedule.generate_fixed_schedule()
        list_of_schedules = schedule.generate_flexible_schedules()
        # There should be 2 possible schedules as we can do laundry on Saturday or Sunday at 9 am start.
        assert len(list_of_schedules) == 2
        # Now test all the diff schedules
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[129]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[130]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[131]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[132]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[133]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[134]) is FlexibleTask
        assert list_of_schedules[0].week.twentyfour_hr_sched[135:168] == [None] * 33
        assert list_of_schedules[0].week.twentyfour_hr_sched[120:129] == [None] * 9
        
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[153]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[154]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[155]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[156]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[157]) is FlexibleTask
        assert type(list_of_schedules[1].week.twentyfour_hr_sched[158]) is FlexibleTask
        assert list_of_schedules[1].week.twentyfour_hr_sched[120:153] == [None] * 33
        assert list_of_schedules[1].week.twentyfour_hr_sched[159:168] == [None] * 9
        
        # the flexible task should not be placed anywhere else either.
        for i in range(120):
            assert type(list_of_schedules[0].week.twentyfour_hr_sched[i]) is not FlexibleTask
            assert type(list_of_schedules[1].week.twentyfour_hr_sched[i]) is not FlexibleTask
    
    # This method tests a more complex generation of scheduling possibilities by adding more times for the
    # flexible tasks to be placed in.
    @staticmethod
    def test_more_complex_backtracking_EarliestSlotStrategy():
        schedule = Scheduler(EarliestSlotStrategy())
        task = TaskFactory.create_task("fixed", "Work", 9, [True, True, True, True, True, True, True], 9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        task2 = TaskFactory.create_task("flexible", "Laundry", 4, None)
        add2 = AddTaskCommand(schedule, task2)
        add2.execute()
        task3 = TaskFactory.create_task("fixed", "Sleep", 9, [True, True, True, True, True, True, True], 0)
        add3 = AddTaskCommand(schedule, task3)
        add3.execute()
        schedule.generate_fixed_schedule()
        list_of_schedules = schedule.generate_flexible_schedules()
        # There should be 105 possible schedules since each day we can start laundry at 18, 19, 20, and multiply that by 7 so 21
        assert len(list_of_schedules) == 21

    # This method tests whether the flexbile tasks are allowed to rollover (they should as if there is an opening
    # between 10 pm and 2 am the next day that opening should be one of the possibilities)
    @staticmethod
    def test_rolloever_in_next_day_EarliestSlotStrategy():
        schedule = Scheduler(EarliestSlotStrategy())
        task = TaskFactory.create_task("fixed", "Work", 9, [True, True, True, True, True, True, True], 9)
        add = AddTaskCommand(schedule, task)
        add.execute()
        task2 = TaskFactory.create_task("flexible", "Laundry", 7, None)
        add2 = AddTaskCommand(schedule, task2)
        add2.execute()
        task3 = TaskFactory.create_task("fixed", "Sleep", 9, [True, False, False, False, False, False, False], 0)
        add3 = AddTaskCommand(schedule, task3)
        add3.execute()
        schedule.generate_fixed_schedule()
        list_of_schedules = schedule.generate_flexible_schedules()
        # The first possibility should roll over so we should have it scheduled from 6 pm monday - 1 am tuesday
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[18]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[19]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[20]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[21]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[22]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[23]) is FlexibleTask
        assert type(list_of_schedules[0].week.twentyfour_hr_sched[24]) is FlexibleTask