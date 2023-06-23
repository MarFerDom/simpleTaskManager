import unittest
import logging
from datetime import datetime, timedelta
from src.task_master import tasks, single_task

logger = logging.getLogger(__name__)


##############################################
#                                            #
#                  EMPTY                     #
#                                            #
##############################################

class TestTasksEmpty(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        self.testing_tasks = tasks.Tasks()


    def test_empty_tasks_valid_index(self):
        '''
           Test empty tasks is_valid_index.
        '''
        logging.info('test_empty_tasks_valid_index')

        # No index should be valid for an empty tasks object.
        for i in [-1,0,1]:
            with self.subTest(i=i):
                self.assertFalse(self.testing_tasks.is_valid_index(i))

        #self.assertIsNotNone(tasks_no_args._buffer)

    def test_empty_tasks_iterator(self):
        '''
           Test empty tasks iterator.
        '''
        logging.info('test_empty_tasks_iterator')

        # Iterator should be empty and raise StopIteration with next
        self.assertRaises(StopIteration, lambda: next(iter(self.testing_tasks)))

    def test_empty_tasks_len(self):
        '''
           Test empty tasks len.
        '''

        logging.info('test_empty_tasks_len')

        # Empty tasks should have length 0
        self.assertEqual(len(self.testing_tasks), 0)
    
    def test_empty_tasks_getitem(self):
        '''
           Test empty tasks getitem.
        '''

        logging.info('test_empty_tasks_getitem')

        # Empty tasks should raise IndexError
        self.assertRaises(IndexError, lambda: self.testing_tasks[0])




##############################################
#                                            #
#              WITH A TASKS                  #
#                                            #
##############################################

class TestTasksAddRemove(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.now = datetime.now()
        self.delta = timedelta(days=1)
        self.data = {
            single_task.TASK_LABELS[0]: 'Tester',
            single_task.TASK_LABELS[1]: 'Test',
            single_task.TASK_LABELS[2]: 'Test Task',
            single_task.TASK_LABELS[3]: (self.now+self.delta).strftime(
                single_task.DATETIME_STRING_FORMAT),
            single_task.TASK_LABELS[4]: self.now.strftime(
                single_task.DATETIME_STRING_FORMAT),
            single_task.TASK_LABELS[5]: 'No',
            }
        
    def setUp(self) -> None:
        self.testing_tasks = tasks.Tasks()
        self.testing_tasks.extend([self.data])

    #########
    # BASIC #
    #########
    def test_add_task(self):
        '''
           Test adding a task.
        '''
        logging.info('test_add_task')

        # Check the task was added.
        self.assertEqual(next(iter(self.testing_tasks)), self.data)

    def test_valid_index(self):
        '''
           Test is_valid_index for valid index 0.
        '''
        logging.info('test_valid_index')

        # With one task index 0 should be valid.
        self.assertTrue(self.testing_tasks.is_valid_index(0))

    def test_len(self):
        '''
           Test len with one task.
        '''
        logging.info('test_len')

        # Should have length 1
        self.assertEqual(len(self.testing_tasks), 1)
    
    ##########
    # ACCESS #
    ##########
    def test_getitem(self):
        '''
           Test getitem.
        '''
        logging.info('test_getitem')

        # One task at index 0
        self.assertIsInstance(self.testing_tasks[0], single_task.SingleTask)

    def test_get_default_value(self):
        '''
           Test getitem with default value.
        '''
        logging.info('test_get_default_value')

        defaut_object = object()
        # One task at index 0
        self.assertIs(self.testing_tasks.get(42, defaut_object), defaut_object)

    ##########
    # REMOVE #
    ##########
    def test_remove_task(self):
        '''
           Test removing a task.
        '''
        logging.info('test_remove_task')

        # Remove only task in index 0.
        self.testing_tasks.remove(0)
        # Iterator should be empty and raise StopIteration with next
        self.assertRaises(StopIteration, lambda: next(iter(self.testing_tasks)))

    def test_does_not_remove_if_wrong_index(self):
        '''
           Test trying to removing wrong index.
        '''
        logging.info('test_does_not_remove_if_wrong_index')

        # Remove only task in index 0.
        self.testing_tasks.remove(1)
        # Iterator should find one task in list.
        iterator = iter(self.testing_tasks)
        self.assertEqual(next(iterator), self.data)
        self.assertRaises(StopIteration, lambda: next(iterator))
    
    ##########
    # UPDATE #
    ##########
    def test_update_task(self):
        '''
           Test updating a task.
        '''
        logging.info('test_update_task')
        # Change original task data to be 'Completed'
        self.data[single_task.TASK_LABELS[-1]] = 'Yes'
        # Show that change only happened in the original data.
        iterator = iter(self.testing_tasks)
        self.assertNotEqual(next(iterator), self.data)
        # Get task object and mark as completed
        task = self.testing_tasks.get(0,single_task.SingleTask())
        task.mark_as_completed()
        # Check that the task is updated before iterating through.
        iterator = iter(self.testing_tasks)
        self.assertEqual(next(iterator), self.data)

    #########
    # STATS #
    #########
    def test_get_stats(self):
        '''
           Test getting stats.
        '''
        logging.info('test_get_stats')

        # Add second tasks
        self.data[tasks.TASK_LABELS[0]] = 'Other'
        self.testing_tasks.extend([self.data])
        # Add third task
        self.testing_tasks.extend([self.data])
        # Mark third task as completed
        self.testing_tasks[2].mark_as_completed() # type: ignore
        # Check stats with two 'Ongoing' and one 'Done'.
        answer = [tasks.STAT_LABELS[2],tasks.STAT_LABELS[2],tasks.STAT_LABELS[0]]
        self.assertEqual(self.testing_tasks.get_stats(), answer)
        