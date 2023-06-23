import logging
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Callable, Mapping

__version__ = 0.1

DATETIME_STRING_FORMAT = "%Y-%m-%d"
DATA_TYPE = Mapping[str,str]

# Title max size in summary.
_TITLE_SHOW_ = 30
# Symbol representing text summarised.
_MORE_ = '...'

# Callback type for flagging task chenges to manager object.
EditCallback = Callable[[], None] #Optional['SingleTask']]

class taskError(ValueError):
    '''
       Error raised when task operation is invalid.
    '''
    ...


@dataclass
class SingleTask():
    '''
       Class representing a single task.

       Attributes:
           owner: str - username of task owner
           title: str - title of task
           description: str - description of task
           due_date: str - date task is due
           assigned_date: str - date task was assigned
           completed: str - 'Yes' if task is

        A callback is bindable for the task editing
        methods to flag changes.
    '''
    owner: str = 'Owner'
    title: str = 'Title'
    description: str = 'Description'
    due_date: str = field(
        default_factory =
            lambda: datetime.today().strftime(DATETIME_STRING_FORMAT)
            )
    datetime.today()
    assigned_date: str = field(
        default_factory =
            lambda: datetime.today().strftime(DATETIME_STRING_FORMAT)
            )
    completed: str = 'No'

    #logging.info('Created single task Owner/Title: {self.owner}/{self.title}')
    callback: EditCallback = field(default=lambda: None, repr=False)

    def bind_edit_flag(self, method: EditCallback):
        '''
           Binds a callback to the task for flagging changes.
        '''
        self.callback = method

    @property
    def data(self) -> DATA_TYPE:
        '''
           Returns task data as a dictionary.
        '''
        dic = asdict(self)
        dic.pop('callback')
        return dic

    @property
    def isOverdue(self) -> bool:
        '''
           Returns True if task is overdue.
        '''
        # Completed tasks are not overdue.
        return not self.isCompleted and \
            datetime.strptime(self.due_date, DATETIME_STRING_FORMAT).date() < \
            datetime.now().date()

    @property
    def isCompleted(self) -> bool:
        '''
           Returns True if task is completed.
        '''
        return self.completed == 'Yes'
    
    @property
    def summary(self) -> str:
        '''
           Returns a summary of the task.
        '''

        # If title is longer than _TITLE_SHOW_, include more symbol.
        more = _MORE_ if len(self.title) > _TITLE_SHOW_ else ''
        # Truncate title and more symbol to _TITLE_SHOW_.
        title = self.title[:(_TITLE_SHOW_-len(more))] + more

        return f'Task: ' + title.ljust(_TITLE_SHOW_) + \
            '\tuser: ' + self.owner + '\tDue date: ' + self.due_date
    
    def __str__(self) -> str:
        '''
           Returns full task description as a string.
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.owner}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date}\n"
        disp_str += f"Due Date: \t {self.due_date}\n"
        disp_str += f"Task Complete?: \t\t {self.completed}\n"
        disp_str += f"Task Description:\n {self.description}\n"
        return disp_str
    
    def is_owned_by(self, owner) -> bool:
        '''
           Checks if provided owner owns this task.

           Returns True if 'owner' is not a string.
        '''
        
        if type(owner) is str:
            return self.owner == owner
        return True
    
##############################################
#                                            #
#             WRITE ATTRIBUTES               #
#                                            #
##############################################

    def mark_as_completed(self) -> None:
        '''
           Mark this task as completed
        '''
        self.completed = 'Yes'
        self.callback()
        logging.info('Marked task {self.title} as completed')

    def edit_user(self, owner:str) -> bool:
        '''
           Update username. Returns True if successful.
        '''
        # Cannot edit completed task
        if self.isCompleted: raise taskError('Completed task cannot be changed')
        # Cannot change to empty owner name
        if len(owner) == 0: raise taskError('Empty new owner name')
        self.owner = owner
        self.callback()
        logging.info('Changed Owner of task {self.title} to: {self.owner}')
        return True

    def edit_date(self, new_date:str) -> bool:
        '''
           Update due_date. Returns True if successful.
        '''
        # Cannot edit completed task
        if self.isCompleted: raise taskError('Completed task cannot be changed')
        # Check if new date is valid
        try:
            datetime.strptime(new_date, DATETIME_STRING_FORMAT)
        except ValueError as e:
            raise taskError(e.args[0])
        self.due_date = new_date
        self.callback()
        logging.info('Changed Due date of task {self.title} to: {self.due_date}')
        return True

# Labels of task data
TASK_LABELS =  list(SingleTask.__dataclass_fields__.keys())
TASK_LABELS.remove('callback')

def valid_filter(data: DATA_TYPE) -> DATA_TYPE:
    '''
       Crops out invalid attributes of data.
    '''

    # Remove empty owner name.
    if len(data['owner']) == 0: data.pop('owner') #type: ignore
    
    # Remove bad formatted dates.
    try:
        datetime.strptime(data['due_date'], DATETIME_STRING_FORMAT)
    except:
        data.pop('due_date') #type: ignore
    try:
        datetime.strptime(data['assigned_date'], DATETIME_STRING_FORMAT)
    except:
        data.pop('assigned_date') #type: ignore

    # Remove completed status different than 'Yes' and 'No'.
    data['completed'] = data['completed'].title() #type: ignore
    if data['completed'] not in ['Yes', 'No']: data.pop('completed') #type: ignore
    
    return data        


# Simple example of how to use this class.
if __name__ == '__main__':

    # Create a task
    data = {k:v for k,v in zip(TASK_LABELS, 'ABC')}
    print(data)
    task = SingleTask(**data) #type: ignore
    print(f'\nCreated task:\n{task}')
    print(f'Summary:\n{task.summary}\n')
    print(f'Is this task completed?: {task.isCompleted}')
    print(f'Is this task overdue?: {task.isOverdue}')
    print(f'As JSON:\n{task.data}\n')

    # Edit task
    task.edit_user('New Owner')
    task.edit_date('2020-01-01')
    # Mark task as completed
    task.mark_as_completed()
    print(f'Task after changes:\n{task}')
    print(f'Is this task overdue?: {task.isOverdue}')
   