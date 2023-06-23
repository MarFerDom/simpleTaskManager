import unittest
import logging
from unittest import mock
from src import protocols
from src import fake
from src.action import controller

logger = logging.getLogger(__name__)

ESCAPE_STATE = 'main menu'
FAKE_STATE = 'fake state'
assert ESCAPE_STATE != FAKE_STATE, \
    "Bad test configuration: states must be different"


class FakeUser(fake.FakeUser):
    @property
    def users(self):
        return iter('fake user')

class TestActionController(unittest.TestCase):
        
    def setUp(self) -> None:
        self.mock_model = mock.Mock()
        return super().setUp()
    
    def test_generate_statistics(self):
        '''
           Tests statistics generation process.
        '''
        
        operation_controller = controller.Controller(
            user=FakeUser(),
            model=self.mock_model,
            id=10,
            next=FAKE_STATE,
            option='generate'
        )

        operation_controller.run()
        # Called just write_report and not mark_as_completed.
        self.mock_model.write_report.assert_called_once()
        self.mock_model.mark_as_completed.assert_not_called()
        # Check state and id are set.
        self.assertEqual(operation_controller.id, -1)
        
    def test_mark_as_completed(self):
        '''
           Tests mark task as completed process.
        '''
        
        operation_controller = controller.Controller(
            user=FakeUser(),
            model=self.mock_model,
            id=10,
            next=FAKE_STATE,
            option='not generate'
        )

        operation_controller.run()
        # Called just mark_as_completed and not write_report.
        self.mock_model.write_report.assert_not_called()
        self.mock_model.mark_as_completed.assert_called_once()
        # Check state and id are set.
        self.assertEqual(operation_controller.id, -1)