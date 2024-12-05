from interpreter import Interpreter, CommandParser, FlexibleTaskParser, FixedTaskParser
from scheduler import ScheduleCommand, Scheduler, AddTaskCommand
from task import TaskFactory
from threading import Thread
from strategy import SchedulingStrategy, EarliestSlotStrategy, SingleTaskPerDayAndStartAt9Strategy
import sys

# Main method, this deals with the CLI interface. 
# The first choice is of the strategy, using the strategy pattern a selected strategy is then passed on to
# the Scheduler class. A while loop allows the
# user to keep entering commands. We then use the interpreter pattern to take in user commands. Either we 
# have a task or a command. For the task we use the factory method to create the task. And then the 
# command pattern to add it (as of now we have adding but this allows for further extensibilty later). 
# If we have a command then depending on the name we complete different actions.
def main():
    print("Starting week scheduler. Please add all the fixed time obligations and then flexible ones.")
    print("This app will schedule the flexible ones around the fixed ones and provide all the different combinations.")
    print("If you would like a certain time blocked just add a fixed time obligation to it that means \"a break\" or something.")
    print("After you are ready to calculate the schedule, type \"calculate\"")
    print("Keep granuality of an hour. Sunday is U, Thursday is R and format for command is")
    print("'fixed TaskName 1 Day(s) [14]' for fixed tasks so type name time in hr which days start time if fixed")
    print("For flexible do flexible TaskName 1 because it just needs time and they don't repeat they are one time things")
    #print(" This will generate up to 20 possible schedules max (if possible)")
    print("First please enter the scheduling strategy: 1 for EarliestSlotStrategy and 2 for SingleTaskPerDayAndStartAt9Strategy")
    int_input = int(input())
    # The first choice is of the strategy, using the strategy pattern a selected strategy is then passed on to
    # the Scheduler class.
    if int_input == 1:
        schedule = Scheduler(EarliestSlotStrategy())
    elif int_input == 2:
        schedule = Scheduler(SingleTaskPerDayAndStartAt9Strategy())
    else:
        print("Invalid strategy, exiting")
        return
    
    print("Now enter tasks")
    user_input = input()
    index = 0
    list_of_schedules = []
    
    while (True):
        interpreter = None
        #task_type, name, duration, start_time, days_of_week = TaskParser.parse(input_str = user_input)
        if (user_input.startswith("flexible")):
            interpreter = FlexibleTaskParser()
        elif (user_input.startswith("fixed")):
            interpreter = FixedTaskParser()
        else:
            interpreter = CommandParser()
        task_type, name, duration, start_time, days_of_week = interpreter.parse(user_input)
        if task_type != "command":
            task = TaskFactory.create_task(task_type, name, duration, days_of_week, start_time)
            add = AddTaskCommand(schedule, task)
            add.execute()
            print("Next task ---")
        else:
            if name == "calculate":
                # now do the calculation of fitting it in schedule, list_of_schedules has all the flexible schedule possiblities.
                schedule.generate_fixed_schedule()
                list_of_schedules = schedule.generate_flexible_schedules()
                print(list_of_schedules)
                print("Type next schedule to keep getting the different combinations of schedules that are possible")
                index = -1
            elif name == "next schedule":
                if len(list_of_schedules) == 0:
                    print("Only fixed tasks provided OR not enough time for any of the flexible tasks, printing out the fixed schedule.")
                    print(schedule.week.print_day_tasks())
                    print("Completed showing schedule, 'next schedule' will print out same one")
                    print("If you would like to save this schedule, enter 'save'")
                elif (index+1 > len(list_of_schedules)):
                    print("End of schedule combinations. Try adding more tasks and calculate again or enter 'calculate' to get the list again.")
                else:
                    # Change index for the next schedule type. 
                    index = index + 1
                    if (index > len(list_of_schedules)):
                        print("End of schedule combinations. Try adding more tasks and calculate again or enter 'calculate' to get the list again.")
                    else:
                        print("-------------------------------------Schedule-------------------------------------------------")
                        print(list_of_schedules[index].week.print_day_tasks())
                        print("Completed showing schedule, enter 'next schedule' for the next combination, it will print out if it exists") 
                        print("If you would like to save this schedule, enter 'save'")
            elif name == "save":
                print("Please provide file name to save schedule to")
                filename = input()
                with open(filename, 'w') as file:
                    file.write(list_of_schedules[index].week.print_day_tasks())
                print("Saved schedule successfully")
                    
            else:
                print("Invalid command entered, please try again.")
        user_input = input()
              
    




if __name__=="__main__":
    main()