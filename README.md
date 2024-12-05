# Overview

This is a schedule helper app that can be run using a GUI interface or through command line. The idea is that you enter in your fixed time appointments (such as work, sleep, scheduled appointments) and then
some tasks that are flexbile but you want them done (for example, laundry as it needs to be done but can be done on any day). This app then calculates the different possibilites of schedules you can have
for the week. You can look through them and save the one(s) you like. There are different strategies that define how tasks are scheduled. Currently we only have two but can add more. The first is earliest slot
strategy which will first start off with filling the tasks in the earliest slot (but all of the possibilites will be visited). The second is Single Task Per Day Start at 9 AM, which will only allow a single flexible
task per day and that only if no Fixed Tasks are already there, so if we are working five days and have not entered sleep, the flexible tasks will be done on the other two days.

## Requirements
- Need a GUI and CLI interface for the user
- User should be able to add fixed and flexible task types
- The fixed tasks will be scheduled to the day and time they are specified
- The program will calculate ALL of the possible ways to complete the flexible tasks while keeping the fixed tasks in place
- The program will present these possible schedules to the user
- The user will be able to save these schedules

## Design and Implementation
There are two different ways that this program is used, either via CLI or GUI. In the CLI, print statements inform the user
of what commands to enter, how to create tasks, and how to save, guiding them through. In the GUI, buttons with labels allow
the user to know what to do and how to navigate.

The GUI uses the tkinter library from Python to create the variety of widgets required. 

In both interfaces, the core of the program remains the same:
First the user chooses a strategy with which to initialize the scheduler. Then the user adds the tasks they want. After that, all
of the fixed tasks are placed in the schedule, and backtracking is done to place all of the flexible tasks in all of the possible
openings. A list of all of these schedules is returned. Then at each 'next schedule' we cycle through all of these possibilites
of schedules and present them to the user. If the user would like to save the schedule, it is printed out to a file whose name 
the user specifies.
## Patterns Used

There are four patterns used in this class, Strategy, Factory Method, Command, and Interpreter.

Strategy
The reason for the strategy pattern is to allow different scheduling strategies. To make this a more hollistic scheduler, there has to be different strategies that cater to the different times that people
want to complete their tasks. For example, the earliest slot is a working strategy and it will actually display all of the different combinations of times that you can perform the tasks, but it can be hard to
find the preferred schedule. What I mean is, lets say I want to focus on work on the weekdays and only do these flexible tasks on the weekends. With the earliest slot strategy, I will get that schedule, but after
lots of 'next schedule' commands because there are just so many possibilities. With the earliest slot strategy, if I am listing work as a fixed task M-F, then the flexible tasks will only be assessed to enter
the schedule on the weekends, saving me the time of finding the schedule I want. The point of this is that the different strategies represent different scheduling algorithms, and they are interchangable to the
rest of the code. Nothing changes if we change strategies in terms of its clients, so it makes sense to encapsulate them so that adding more strategies is easy. All I need to do is create a new class that implements
SchedulingStrategy and add that as a list of options for the user to choose. Again the choosing of different strategies really help make this app 'better' as it allows custom scheduling based on the users' preferenes,
so even though we only have two right now the addition of more is expected and it will be much easier to add if we have this decoupling that we get from the strategy pattern. The use case was so similar to the textbook
case for strategy pattern that other patterns weren't really feasible for this particular piece. However, the template method pattern did seem like a second because we could use inheritance and since as of now only the
get_available_slots method different in between the strategies, the template method could be a super class and each of the specific strategies could have their own implementation of get_available_slots. However, I chose
strategy because I did not want to have excessive coupling and control by the super class. Also, there isn't really a use of hook methods and the sequence steps that are commonly present in the template method pattern,
so its real use would not be realized here.

Factory Method
This pattern is used for the creation of the types of tasks, fixed and flexible. The use of this decouples the creation from
the use of the object. The main reason to do this is because right now we only have two task types, but in the future if that
was to be made more extensible, it would make sense to decouple because then the main code would not need extensive changes.
All that would be needed was adding a new type of Task that follows the interface rules. The tasks have different parameters
and their creation is complex, but they all implement an interface, which are reasons to decouple this and allow the factory
to take care of the creation. The task factory just reads the type and creates the appropriate type of task, keeping us from
having to put this checking and if statements in the main method, keeping the code cleaner. The other pattern that could have
been used was the Builder pattern, however, that is used more for complex objects that have a lot of parts, and we can use
the builder pattern to create it step by step. However, for my case that was not needed because the task objects just had
fields that had to be initialized, but not really steps that had to be done to create the object.

Command Pattern
This pattern is used to manage the schedule. Currently, we have the AddTaskCommand, which is an external class that separates the addition of a task to a schedule from the schedule class itself. This decoupling
is used mostly because it will allow for more commands in the future, such as ones that can swap tasks, remove tasks, etc. The scheduler class is for the most part fixed, and so I don't want to have to change
that later, so it makes more sense to use the command pattern that will allow for more extensibility when new commands are added, and the scheduler class can remain unchanged. The command pattern is useful because
I can also have undo/redo operations, because currently that is not a feature but if I would like to add to the app and support such a feature, I can do so. I can
also retain a history of the different commands executed. This was the main reason for the command pattern being used. Although other methods and patterns could
have been used for decoupling, an interesting and useful part of the command pattern is that saving of history, which I wanted to be able to have redo/undo operations
in the future.


Interpreter Pattern
The reason for this pattern was for interpreting the command line arguments and also the UI arguments. The user either enters the required fields for the task (name, duration, etc.) in a string or in the input
boxes in the UI. Then it is up to the interpreter to interpret these. If the user enters a command such as 'save' or 'next schedule' that also is interpreted by the interpreter (there are different classes that are used for each that all have the interpret method). This way a standardized method interpret is called whenever we need the parameters the user provided (in terms of tasks) or the information about the command
(if it is a command). This can then be used to direct the actions of the CLI/GUI. The use of this pattern for commands is less in the GUI because those commands are now known because each button only is linked to one command, but it is much more useful in the command line. In the CLI, there is a 'language' that the user is following when entering these commands (that is specified to the user when they are adding tasks,
so having an interpreter translate that into method calls is critical because tasks and commands are all built from these user inputs. Having an interpreter allows for the main method to just create an object of the type that implements Interpreter, and then use the interpret method (which in my case is called parse) to get the required fields that can be used to create a task or execute a command. In the GUI, this interpreter
is still used and sent as a stub to a method called interpreter, which takes it and calls the interpret method and based on the result performs different tasks. The use of this pattern was to avoid nested if statements that would be needed to interpret user commands in the CLI, along with the fact that adding more commands and tasks is relatively easy. If we did not use this pattern then we would have to directly go into if
statements in the code that deals with the parsing of the user commands, but with this pattern all we have to do is create a new class that implements Interpreter and use that. The method parse will have to be in that class and the main method can just call it, as it does with the existing classes that we currently have that implement Interpreter. Another pattern I had in mind was the state pattern, because that would 
have a state machine and either the user could go to the command state or the task state. If in the command state, the user would just specify the name of the command, and if in the task state first the user
would have to specify fixed or flexible, then the parameters. However, the reason I went against this was because I wanted there to be a way for the user to just initialize the task in a single line or in terms of the UI a single button press.
I did not want to have to have a series of questions being asked to slowly go from one state to another until we created a task when we had all the values needed. Similarly with the UI, I just wanted the user to enter in the fields and press the button and the app read the values they provided and understood that as a task. I also realized that with the addition of newer types of tasks, that would be harder
because the whole state machine would need to be modified and inserted with all the different steps needed to make that new type of task.

## Running the Tests

The tests for the assignment are contained in the test_final.py 
class. You can run this class as a pytest test in your IDE or from the 
command line using "pytest". Every time that you commit and push
to GitHub, GitHub Actions will compile and test your code. You can 
view the results on the "Actions" tab in your GitHub repository.
