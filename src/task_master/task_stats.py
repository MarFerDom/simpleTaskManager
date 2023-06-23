import logging
from typing import List, Mapping, Optional, Tuple
from src.task_master.tasks import DATA_TYPE, TASK_LABELS, STAT_LABELS

__version__ = 0.1

########################################################
#                   MEMBERS                            #
########################################################
#
# 1. CONST
##
# USER_REPORT_LABELS: List[str]
# TASK_REPORT_LABELS: List[str]
##
# 2. FUNCTION
##
# pcent: Callable[[float,float],float]
##
# 3. CLASS
##
# TaskStats: Calculates statistics for given task data.
#   Properties:
#   - users_stats: List of statistics per user.
#   - tasks_stats: Aggregated statistics for all users.
########################################################



##########
# LABELS #
##########
_BASE_LABELS = ['username', 'Total tasks']
_REPO_LABELS = _BASE_LABELS + STAT_LABELS + \
                [condition+'(%)' for condition in STAT_LABELS]
_NUMBER_OF_USERS = 'Users'

# Index to start absolute value attributes
_BASE_INDEX = len(_BASE_LABELS)
# Index to start percentage attributes
_PCNT_INDEX = len(STAT_LABELS) + _BASE_INDEX

# Type for statistics
_STATS_TYPE = Mapping[Tuple[str,str],int]

##############################################################################
def pcent(num, total) -> float:
    '''
       Helper function to get percentage of integer values.
    '''
    
    if num <0 or total < num: raise ValueError
    return 100.*num/max(total,1)

class TaskStats():
    '''
       Task statistics class.

       Calculates statistics for given task data.

       Parameters:
       - buffer: List of task data.
       - stats: List of status to calculate statistics for.
       - userlist: List of users to calculate statistics for. If None all users
                   in buffer are used.

       Properties:
       - users_stats: List of statistics per user.
       - tasks_stats: Aggregated statistics for all users.
    '''

    def __init__(self,
                buffer:List[DATA_TYPE],
                stats: List[str],
                userlist: Optional[List[str]] = None,
                *args, **kwargs) -> None:
        
        super(TaskStats, self).__init__(*args, **kwargs)
        self._stats: _STATS_TYPE = self._get_status(buffer, stats)
        # If no user list get all users from buffer.
        self.userlist = userlist or set([data[TASK_LABELS[0]]
                                       for data in buffer])
        # Holds last response to user_statistics
        self._users: Optional[List[DATA_TYPE]] = None
        # Holds last response to task_statistics
        self._tasks: Optional[DATA_TYPE] = None
        logging.info(f'Created {self.__class__} with ' + \
                     f'{"no " if userlist is None else ""}userlist')

    @property
    def users_stats(self):
        if self._users is None: self.user_statistics()
        return self._users
    
    @property
    def tasks_stats(self) -> DATA_TYPE:
        if self._tasks is None: self.task_statistics()
        return self._tasks #type:ignore

    def _get_status(self, buffer: List[DATA_TYPE], stats: List[str]) -> _STATS_TYPE:
        '''
           For each data entry counts (user, status) pairs.
        '''

        logging.info(f'Running {self._get_status.__name__}')

        data_counts = {}
        # For each data entry in buffer and related stats
        for data, stat in zip(buffer, stats):
            # Create a key with username and status
            key = (
                data[TASK_LABELS[0]],
                stat
            )
            # For every key add 1 to count.
            # If non existing a new one starts with 0 counts.
            data_counts.update({
                key: data_counts.get(key,0)+1
            })

        logging.info(f'{self._get_status.__name__} completed with {len(data_counts)} entries')
        return data_counts
    

    def user_statistics(self) -> None:
        '''
           Calculates task statistics per user as list.

           Sets value for user_stats property
        '''

        logging.info(f'Running {self.user_statistics.__name__}')

        self._users = []
        # For each user in the list
        for user in self.userlist:

            # Get number of tasks in each condition for this user.
            quantity = dict.fromkeys(STAT_LABELS, 0)
            for condition in STAT_LABELS:
                quantity[condition] = self._stats.get((user, condition), 0)

            # Create a line with user and total number of tasks.
            sum_user = sum(quantity.values())
            line = {
                _REPO_LABELS[0]:user,
                _REPO_LABELS[1]:str(sum_user),
            }

            # Insert quantity for each condition
            line.update(
                {k:str(v) for k,v in
                    zip(_REPO_LABELS[_BASE_INDEX:], quantity.values())}
                )
            # Insert percentages of total for each condition
            line.update(
                {k:f'{pcent(v,sum_user):1.2f}' for k,v in
                    zip(_REPO_LABELS[_PCNT_INDEX:], quantity.values())}
                )            
            # Include current users' line
            self._users.append(line)

        logging.info(f'{self.user_statistics.__name__} completed with {len(self._users)} entries')


    def task_statistics(self) -> None:
        '''
           Calculates aggregated task statistics for whole user base.

           Sets value for task_stats property.
        '''
        
        logging.info(f'Running {self.task_statistics.__name__}')
        
        output = {}
        output.update({_REPO_LABELS[2]:0})
        output.update({_REPO_LABELS[3]:0})
        output.update({_REPO_LABELS[4]:0})

        # Total number of users
        output.update({_NUMBER_OF_USERS: len(self.users_stats or [])})

        # Sum of tasks in each status
        for data in self.users_stats or []:
            output[_REPO_LABELS[2]] += int(data[_REPO_LABELS[2]])
            output[_REPO_LABELS[3]] += int(data[_REPO_LABELS[3]])
            output[_REPO_LABELS[4]] += int(data[_REPO_LABELS[4]])

        # Total sum of tasks in all status
        output[_REPO_LABELS[1]] = output[_REPO_LABELS[2]] + \
                                 output[_REPO_LABELS[3]] + \
                                 output[_REPO_LABELS[4]]
        
        output.update({_REPO_LABELS[5]:0.})
        output.update({_REPO_LABELS[6]:0.})
        output.update({_REPO_LABELS[7]:0.})
        # Percentages are calculated from total sum
        output[_REPO_LABELS[5]] = pcent(output[_REPO_LABELS[2]], output[_REPO_LABELS[1]])
        output[_REPO_LABELS[6]] = pcent(output[_REPO_LABELS[3]], output[_REPO_LABELS[1]])
        output[_REPO_LABELS[7]] = pcent(output[_REPO_LABELS[4]], output[_REPO_LABELS[1]])

        # Return with values as strings
        self._tasks = {k:f'{v}' if type(v) is int else f'{v:1.2f}' for k,v in output.items()}
        logging.info(f'{self.task_statistics.__name__} completed with {len(self._tasks)} entries')


######################
# Labels for reports #
######################

USER_REPORT_LABELS = _REPO_LABELS
TASK_REPORT_LABELS = [_NUMBER_OF_USERS] + _REPO_LABELS[1:]