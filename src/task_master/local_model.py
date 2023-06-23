import logging
from typing import List, Optional, Tuple
from src import plugin
from src import config, user_manager
from src.task_master import single_task, tasks, task_stats

try:
    DataFile = plugin.get_class(config.FILE_HANDLER)
    ReportFile = plugin.get_class(config.REPORT_HANDLER)
except Exception as e:
    logging.error("Could not load modules defined in config.py")
    print(e.args[0])
    exit(-1)

class Model():
    '''
       Class that connects the file handling, the tasks
       handling and the task statistics generation.
    '''

    def __init__(self,
                 taskfile: str = config._TASK_FILE_,
                 u_report_file: str = config._USER_REPORT_FILE_,
                 t_report_file: str = config._TASK_REPORT_FILE_
                 ) -> None:
        self.tasks = tasks.Tasks()

        # Create file handlers
        self.taskfile = DataFile(taskfile, labels=tasks.TASK_LABELS)

        self.user_report_file = ReportFile(
            filename=u_report_file,
            labels=task_stats.USER_REPORT_LABELS)
        
        self.task_report_file = ReportFile(
            filename=t_report_file,
            labels=task_stats.TASK_REPORT_LABELS)
        
        # Load tasks data from file.
        self.taskfile.load()

        # Update tasks list with data from file.
        self.tasks.extend(self.taskfile.buffer)
        
    def get_all_tasks(self, user: Optional[str] = None) -> Tuple[List[str], List[int]]:
        '''
           Returns all the tasks associated to a user and a mapping to real task index.
           If no user is specified, returns all tasks.
        '''

        return self.tasks.list_tasks(user)

    def get_task(self, index: int) -> str:
        '''
           Returns full text description of a task.
        '''

        return str(self.tasks[index])

# TASK EDITING AND READING

    def add_task(self, data:List[str]) -> bool:
        '''
           Delegate task inclusion to Tasks class.
        '''

        self.tasks.extend([{k:v for k,v in zip(tasks.TASK_LABELS, data)}])
        return True

    def mark_as_completed(self, task_id:int) -> None:
        '''
           Marks a task as completed.
        '''

        try:
            self.tasks[task_id].mark_as_completed()
        except IndexError:
            pass

    def is_task_completed(self, task_id:int) -> bool:
        '''
           Check task completion.
        '''

        try:
            return self.tasks[task_id].isCompleted
        except IndexError:
            pass
        return False

    def edit_user(self, task_id:int, owner:str) -> bool:
        '''
           Delegates user change to Tasks class.
        '''

        try:
            return self.tasks[task_id].edit_user(owner) # type: ignore
        except IndexError or single_task.taskError:
            return False

    def edit_date(self, task_id:int, date:str) -> bool:
        '''
           Delegates user change to Tasks class.
        '''

        try:
            return self.tasks[task_id].edit_date(date) # type: ignore
        except IndexError or single_task.taskError:
            return False

    def save_tasks(self):
         '''
            Saves task changes to file.
         '''

         self.taskfile.buffer.clear()
         self.taskfile.buffer.extend(iter(self.tasks))
         self.taskfile.dump()

# REPORT GENERATING AND READING

    def read_report(self, userlist: List[str]) -> str:
        '''
           Returns content of two reports files.
        '''
        
        self.write_report(userlist)
        return str(self.user_report_file) + '\n'*3 + \
            'Task statistics:\n\n' + str(self.task_report_file)

    def save_user_report(self, report: List[task_stats.DATA_TYPE]):
         '''
            Saves user report data to file.
         '''
         
         self.user_report_file.buffer.clear()
         self.user_report_file.buffer.extend(report)
         self.user_report_file.dump()

    def save_task_report(self, report: List[task_stats.DATA_TYPE]):
         '''
            Saves task report data to file.
         '''
         
         self.task_report_file.buffer.clear()
         self.task_report_file.buffer.extend([report])
         self.task_report_file.dump()

    def set_report_headers(self, number_users: str, number_tasks: str) -> None:
        '''
           Sets file header with number of users and tasks.
        '''

        # Set USER_REPORT_FILE's header with number of users and tasks.
        pre_header =  "-----------------------------------\n" + \
                     f"Number of users: \t\t {number_users}\n" + \
                     f"Number of tasks: \t\t {number_tasks}\n" + \
                      "-----------------------------------\n" + \
                      "\nUser statistics:\n"
        self.user_report_file.set_pre_header(pre_header)

    def write_report(self, userlist: List[str]) -> None:
        '''
           Returns users and tasks statistics.
        '''

        # Creates a report generator and returns users and tasks reports.
        task_stats_calc = task_stats.TaskStats(
            [*iter(self.tasks)],
            self.tasks.get_stats(),
            userlist
        )

        # Pass total number of users and tasks to report file headers.
        self.set_report_headers(
            number_users=\
                task_stats_calc.tasks_stats[task_stats.TASK_REPORT_LABELS[0]],
            number_tasks=\
                task_stats_calc.tasks_stats[task_stats.TASK_REPORT_LABELS[1]]
        )

        # Saves reports to files.
        self.save_user_report(task_stats_calc.users_stats) #type: ignore
        self.save_task_report(task_stats_calc.tasks_stats) #type: ignore


if __name__ == '__main__':
    users = user_manager.UserManager()
    model = Model()
    tasks_to_add = [
        {
            single_task.TASK_LABELS[0]: 'tester',
            single_task.TASK_LABELS[1]: 'Test 1',
            single_task.TASK_LABELS[2]: 'Test Task 1'
        },
        {
            single_task.TASK_LABELS[0]: 'admin',
            single_task.TASK_LABELS[1]: 'Test 2',
            single_task.TASK_LABELS[2]: 'Test Task 2'
        }
    ]
    #model.add_task(tasks_to_add) #type: ignore
    #model.save_tasks()
    #model.write_report(list(users.users))
    #print(model.read_report())

    text, mapping = model.get_all_tasks('admin')
    print(text)
    print('\nPrior to change:')
    print(model.get_task(mapping[3]))
    print('\nAfter date change:')
    model.edit_date(mapping[3], '2024-01-01')
    print(model.get_task(mapping[3]))
    print('\nAfter owner change')
    model.edit_user(mapping[3], 'D.A.')
    print(model.get_task(mapping[3]))
    print('\nAfter marked as completed')
    model.mark_as_completed(mapping[3])
    print(model.get_task(mapping[3]))
    # if not model.save_tasks no change is saved.