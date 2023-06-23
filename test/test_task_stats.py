import unittest
import logging
from typing import List

from src.task_master import task_stats

logger = logging.getLogger(__name__)

class TestTaskStats(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        ##################
        #   MOCK INPUT   #
        ##################

        # A list of tasks with two users.
        self.task_list: List[task_stats.DATA_TYPE] = [
            {
                task_stats.TASK_LABELS[0]: 'Person1',
                task_stats.TASK_LABELS[1]: 'Task1'
            },

            {
                task_stats.TASK_LABELS[0]: 'Person2',
                task_stats.TASK_LABELS[1]: 'Task2'
            },

            {
                task_stats.TASK_LABELS[0]: 'Person1',
                task_stats.TASK_LABELS[1]: 'Task3'
            },
        ]

        # List of status
        self.stats = [
            task_stats.STAT_LABELS[0],
            task_stats.STAT_LABELS[0],
            task_stats.STAT_LABELS[1]
            ]
        
        ##################
        # CORRECT OUTPUT #
        ##################

        # Supposed output for TaskStats(task_list, stats)._stats
        self.stats_answer = {
            ('Person1', task_stats.STAT_LABELS[0]): 1,
            ('Person2', task_stats.STAT_LABELS[0]): 1,
            ('Person1', task_stats.STAT_LABELS[1]): 1
        }

        # Supposed output for TaskStats(task_list, stats).users_stats
        self.users_answer = [dict.fromkeys(task_stats.USER_REPORT_LABELS, '0') for _ in range(2)]
        self.users_answer[0][task_stats.USER_REPORT_LABELS[0]] = 'Person1'
        self.users_answer[0][task_stats.USER_REPORT_LABELS[1]] = '2'
        self.users_answer[0][task_stats.USER_REPORT_LABELS[2]] = '1'
        self.users_answer[0][task_stats.USER_REPORT_LABELS[3]] = '1'
        self.users_answer[0][task_stats.USER_REPORT_LABELS[5]] = '50.00'
        self.users_answer[0][task_stats.USER_REPORT_LABELS[6]] = '50.00'
        self.users_answer[0][task_stats.USER_REPORT_LABELS[7]] = '0.00'

        self.users_answer[1][task_stats.USER_REPORT_LABELS[0]] = 'Person2'
        self.users_answer[1][task_stats.USER_REPORT_LABELS[1]] = '1'
        self.users_answer[1][task_stats.USER_REPORT_LABELS[2]] = '1'
        self.users_answer[1][task_stats.USER_REPORT_LABELS[5]] = '100.00'
        self.users_answer[1][task_stats.USER_REPORT_LABELS[6]] = '0.00'
        self.users_answer[1][task_stats.USER_REPORT_LABELS[7]] = '0.00'

        # Supposed output for TaskStats(task_list, stats).tasks_stats
        self.tasks_answer = dict.fromkeys(task_stats.TASK_REPORT_LABELS, '0.00')
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[0]] = '2'
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[1]] = '3'
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[2]] = '2'
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[3]] = '1'
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[4]] = '0'
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[5]] = '66.67'
        self.tasks_answer[task_stats.TASK_REPORT_LABELS[6]] = '33.33'
        self.tasks_answer

    def setUp(self) -> None:
        self.testing_tasks_stats = task_stats.TaskStats(self.task_list, self.stats)

    def test_get_status(self):
        '''
           Test _status property.
        '''
        logging.info('test_get_status')

        # Compare with correct output.
        self.assertEqual(self.testing_tasks_stats._stats, self.stats_answer)


    def test_users_stats(self):
        '''
           Test user_stats property.
        '''
        logging.info('test_users_stats')

        # Compare with correct output.
        self.assertCountEqual(self.testing_tasks_stats.users_stats or [], self.users_answer)

    def test_tasks_stats(self):
        '''
           Test task_stats property.
        '''
        logging.info('test_tasks_stats')

        # Compare with correct output.
        self.assertDictEqual(self.testing_tasks_stats.tasks_stats or {}, self.tasks_answer)

if __name__ == '__main__':
    unittest.main()