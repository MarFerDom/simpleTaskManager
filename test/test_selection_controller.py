import unittest
import logging
from unittest import mock
from src import protocols
from src.fake import FakeUser
from src.selection import controller
from src.selection.example import FakeModel

logger = logging.getLogger(__name__)


ESCAPE_STATE = 'main menu'

mock_view = mock.MagicMock()
options, mapping = FakeModel().get_all_tasks()

class TestSelectionController(unittest.TestCase):

    def setUp(self) -> None:
        self.operation_controller = controller.Controller(
            user=FakeUser(),
            model=FakeModel(),
            id=-1,
            source='user',
            next='fake state',
            options=['a', 'b', 'c']
        )
        return super().setUp()

    def tearDown(self) -> None:
        mock_view.reset_mock()
        return super().tearDown()
    
##############################################
#                                            #
#             INITIALIZATION                 #
#                                            #
##############################################
    
    def test_options_from_source_user(self):
        '''
           Tests that options from source='user'.
        '''
        
        # Options and mapping from FakeModel.get_all_tasks not the initializer.
        self.assertCountEqual(
            ['{} - {}'.format(i+1,options[i]) for i in range(len(options))],
            self.operation_controller.options)
        self.assertCountEqual(
            mapping,
            self.operation_controller.mapping)
        
    def test_options_from_initializer(self):
        '''
           Tests that options from initializer.
        '''
        
        local_options = ['a', 'b', 'c']
        operation_controller = controller.Controller(
            user=FakeUser(),
            model=FakeModel(),
            id=-1,
            source='not user',
            options=local_options
        )
        # Options come from the initializer.
        self.assertCountEqual(
            local_options,
            operation_controller.options)
        self.assertFalse(hasattr(operation_controller,'mapping'))

    def test_no_view_binded_run_error(self):
        '''
           Tests that running without binding a view raises and error.
        '''

        self.assertRaises(protocols.ControllerError, self.operation_controller.run)


##############################################
#                                            #
#               RUNNING                      #
#                                            #
##############################################

    def test_normal_run(self):
        '''
           Test running with no view interaction.
        '''

        self.operation_controller.bind_UI(lambda **_: mock_view) #type: ignore
        self.operation_controller.run()
        # Assert view's methods are called.
        mock_view.mainloop.assert_called_once()
        mock_view.bind_provider.assert_called_once()

    def test_selection_from_user(self):
        '''
           Test next state and task id update after calling select.
        '''

        # When source='user' the operation is 'view mine':
        #   - next is defined at initialization
        #   - id is the index of the option selected
        for i in range(len(options)):
            with self.subTest(i=i):
                self.operation_controller.select(i)
                self.assertEqual(
                    self.operation_controller.next,
                    'fake state'
                )
                self.assertEqual(
                    mapping[i],
                    self.operation_controller.id
                )
    
    def test_selection_from_initializer(self):
        '''
           Test next state and task id update after calling select.
        '''

        local_options = ['a', 'b', 'c']
        operation_controller = controller.Controller(
            user=FakeUser(),
            model=FakeModel(),
            id=-1,
            source='not user',
            options=local_options
        )

        # When source='not user' the operation is 'menu':
        #   - next is the option selected
        #   - id does not change
        for i in range(len(local_options)):
            with self.subTest(i=i):
                old_id = operation_controller.id
                operation_controller.select(i)
                self.assertEqual(
                    operation_controller.next,
                    local_options[i]
                )
                self.assertEqual(
                    operation_controller.id,
                    old_id
                )

    def test_escape(self):
        '''
           Test escape entry [-1].
        '''

        # When source='user' the operation is 'view mine':
        #   - next is defined at initialization
        #   - id is the index of the option selected
        self.operation_controller.select(-1)
        self.assertEqual(
            self.operation_controller.next,
            ESCAPE_STATE
        )
        self.assertEqual(
            -1,
            self.operation_controller.id
        )