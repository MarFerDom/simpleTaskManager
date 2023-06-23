import unittest
from unittest import mock
import logging
from datetime import datetime, timedelta
from src.task_master import single_task

logger = logging.getLogger(__name__)


##############################################################################
##############################################
#                                            #
#             task.SingleTask                #
#                                            #
##############################################
class TestSingleTask(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.now = datetime.now()
        self.delta = timedelta(days=1)
        self.data = {
            single_task.TASK_LABELS[0]: 'Tester',
            single_task.TASK_LABELS[1]: 'Test',
            single_task.TASK_LABELS[2]: 'Test Task',
            single_task.TASK_LABELS[3]: (self.now+self.delta).strftime(single_task.DATETIME_STRING_FORMAT),
            single_task.TASK_LABELS[4]: self.now.strftime(single_task.DATETIME_STRING_FORMAT),
            single_task.TASK_LABELS[5]: 'No',
            }
        
    def setUp(self) -> None:
        self.testing_task = single_task.SingleTask(**self.data) # type: ignore
        return super().setUp()

    def test_is_not_completed(self):
        '''
           Test 'complete' property.
        '''
        logging.info('test_is_not_completed')

        # Task is not complete.
        self.assertFalse(self.testing_task.isCompleted)
        self.assertEqual(self.testing_task.completed, 'No')

    def test_mark_as_completed(self):
        '''
           Test mark_as_completed method and 'complete' property.
        '''
        logging.info('test_mark_as_completed')

        self.testing_task.mark_as_completed()
        # Task is now complete.
        self.assertTrue(self.testing_task.isCompleted)
        self.assertEqual(self.testing_task.completed, 'Yes')

    def test_edit_user(self):
        '''
           Test editing user.
        '''
        logging.info('test_edit_user')

        new_user = 'Douglas Adams'
        self.assertTrue(
            self.testing_task.edit_user(new_user))
        # Task username is now 'Douglas Adams'.
        self.assertEqual(self.testing_task.owner, 'Douglas Adams')
    
    def test_edit_due_date(self):
        '''
           Test editing due date.
        '''
        logging.info('test_edit_due_date')

        new_date = '1979-10-12'
        self.assertTrue(
            self.testing_task.edit_date(new_date))
        # Task username is now 'Douglas Adams'.
        self.assertEqual(self.testing_task.due_date, '1979-10-12')

    def test_not_edit_completed(self):
        '''
           Test completed task editing error exception raising.
        '''
        logging.info('test_not_edit_completed')

        new_user = 'Douglas Adams'
        new_date = '1979-10-12'
        self.testing_task.mark_as_completed()

        # Editing must raise exception for completed task.
        self.assertRaises(single_task.taskError,
            self.testing_task.edit_user, new_user) # type: ignore
        self.assertRaises(single_task.taskError,
            self.testing_task.edit_date, new_date) # type: ignore
        
        # Task username and due date should not have changed.
        self.assertNotEqual(self.testing_task.owner, 'Douglas Adams')
        self.assertNotEqual(self.testing_task.due_date, '1979-10-12')

    def test_not_edit_empty_owner_name(self):
        '''
           Test bad owner name error exception raising.
        '''
        logging.info('test_not_edit_empty_owner_name')

        new_user = ''
        
        # Bad owner name exception should be raised.
        self.assertRaises(single_task.taskError,
            self.testing_task.edit_user, new_user) # type: ignore
        
        # Task username should not have changed.
        self.assertNotEqual(self.testing_task.owner, '')

    def test_not_edit_bad_date(self):
        '''
           Test bad date error exception raising.
        '''
        logging.info('test_not_edit_bad_date')

        new_date = '42-42-42'
        
        # Bad date exception should be raised.
        self.assertRaises(single_task.taskError,
            self.testing_task.edit_date, new_date) # type: ignore
        
        # Task due date should not have changed.
        self.assertNotEqual(self.testing_task.owner, '42-42-42')

    def test_edit_callback(self):
        '''
           Test callback assignment.
        '''
        logging.info('test_edit_callback')
        mock_call = mock.MagicMock()
        self.testing_task.bind_edit_flag(mock_call)
        new_user = 'Douglas Adams'
        new_date = '1979-10-12'

        # Editing must return True if successful.
        self.assertTrue(self.testing_task.edit_user(new_user))
        self.assertTrue(self.testing_task.edit_date(new_date))
        self.testing_task.mark_as_completed()

        # Task username and due date should not have changed.
        self.assertEqual(mock_call.call_count, 3)

    def test_data_attribute(self):
         '''
            Test data attribute.
         '''
         logging.info('test_data_attribute')

         # Data attribute must be a dictionary.
         self.assertIsInstance(self.testing_task.data, dict)
         self.assertEqual(self.testing_task.data, self.data)