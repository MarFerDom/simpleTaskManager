import logging
from typing import Any, List, Optional, Tuple
from src.task_master.single_task import SingleTask, taskError, valid_filter, DATA_TYPE, TASK_LABELS

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

# Labels for task status
STAT_LABELS = ['Done', 'Overdue', 'Ongoing']

class Tasks():
    '''
       Class manages list of tasks.

       Maintains a list of tasks as DATA_TYPE.
       Creates a SingleTask object for each entry manipulation.
       After editing the SingleTask object, corresponding list item is updated.
       Changes are flushed when other task is accessed or flush() is called.

       Attributes:
       - _buffer: List of tasks as DATA_TYPE.
       - _cursor: Cursor to current task.
       - _changed: Marker to check if task was changed.
       - _task: Pointer to task.
    '''

    def __init__(self, *args, **kwargs):
        super(Tasks, self).__init__(*args, **kwargs)
        # List of tasks as DATA_TYPE.
        self._buffer: List[DATA_TYPE] = list()
        # Cursor to current task.
        self._cursor: int = 0
        # Marker to check if task was changed.
        self._changed: bool = False
        # Pointer to task.
        self._task: Optional[SingleTask] = None


##############################################
#                                            #
#             TASKS DATA LIST                #
#                                            #
##############################################
        
    def __iter__(self) -> Any:
        '''
           Get iterator of DATA_TYPE items in list.
        '''

        # update from working task before returning iterator.
        self._update()
        return iter(self._buffer)
    
    def __len__(self) -> int:
        '''
           Returns number of tasks in list.
        '''

        return len(self._buffer)

    def extend(self, tasks_data: List[DATA_TYPE]) -> None:
        '''
           Adds new task ignoring invalid keys.

           Skips failed task creation.

           Arguments:
           - tasks_data:
                List of dictionaries with keys: username,title,..,due_date.
        '''

        for data in tasks_data:
            try:
                # Create task object and add to buffer
                self._buffer.append(SingleTask(**valid_filter(data)).data) #type: ignore
                
            except taskError as e:
                # Logs warning if task creation fails
                logger.warning(f'''Unable to insert task due to:
                              {e.args[0]}
                              Data dump:
                              {data}''')

    def is_valid_index(self, index: int) -> bool:
        '''
           Checks for index in range [0, len(tasks)-1]
        '''

        return len(self) > index >= 0
    
    def remove(self, index: int) -> None:
        '''
           Removes task in 'index'.
        '''

        # Removes task in valid index.
        if self.is_valid_index(index):
            # If removing current working task, flush task.
            if self._cursor == index: self.flush()
            # If removing from lower index, adjust cursor.
            if self._cursor > index: self._cursor -= 1
            # Remove task from list.
            self._buffer.pop(index)
        
##############################################
#                                            #
#         SINGLE TASK MANIPULATION           #
#                                            #
##############################################

    def _edit_flag(self):
        '''
           To be used as callback for changing tasks.
        '''

        self._changed = True

    def _update(self):
        '''
           Updates list from current working task object.
        '''

        # If no task or change, return.
        if self._task is None or not self._changed: return

        # Updates data in list and resets flag.
        self._buffer[self._cursor] = self._task.data
        self._changed = False

    def flush(self):
        '''
           Updates data in buffer[cursor] from task object and release it.

           Skips if no changes or no task.
        '''

        if self._task is None: return
        
        # Update from working task.
        self._update()
        # Remove binded method to stop rougue calls.
        self._task.bind_edit_flag(lambda: None)
        # Release task object from tasks.
        self._task = None

    def _change_cursor(self, index: int) -> None:
        '''
           Follow steps for changing cursor position.

           Steps:
           - Updates task if changed.
           - Releases task after unbinding flag callback.
           - Sets cursor to 'index'
           - Returns self.
        '''
        # If same index return.
        if index == self._cursor: return

        # Checks for valid index.
        if not self.is_valid_index(index):
            logger.warning("Index out of bounds: No changes made.")
            raise IndexError("Invalid index")
        
        # Update changes in task if there are any.
        self.flush()
        
        # Set cursor to new index.
        self._cursor = index

    def __getitem__(self, index: int) -> SingleTask:
        '''
           Returns SingleTask object associated with task in 'index'.
        '''
        
        # Sets cursor to index position and tests for task change.
        self._change_cursor(index)
        # If same index, returns existing object otherwise create new.
        if self._task is None:
            # If task changed create task object and bind to flag method.
            self._task = SingleTask(**(self._buffer[self._cursor]))#type:ignore
            self._task.bind_edit_flag(self._edit_flag)

        return self._task
    
    def get(self, index: int=0, default: Any=None) -> Any:
        '''
           Returns task data in 'key' or default value.
        '''

        if self.is_valid_index(index):
            return self[index]
        else:
            return default
        
    def list_tasks(self, owner:Optional[str] = None) -> Tuple[List[str],List[int]]:
        '''
           Returns string of all tasks in list and their indices.
        '''

        self._update()
        out = []
        index = []
        for i in range(len(self)):
            task = self[i]
            if task.is_owned_by(owner):
                out.append(task.summary+f"\tStatus: {self._stats(i)}")
                index.append(i)
        return out, index

##############################################
#                                            #
#             TASK LIST STATUS               #
#                                            #
##############################################

    def _stats(self, i: int) -> str:
        '''
           Returns the status code of task in 'index'.
        '''

        task = self[i]
        if task.isCompleted:
            return STAT_LABELS[0]
        if task.isOverdue:
            return STAT_LABELS[1]
        return STAT_LABELS[2]
    
    def get_stats(self) -> List[str]:
        '''
           Returns the status code for all tasks
        '''

        self.flush()
        return [self._stats(i) for i in range(len(self))]