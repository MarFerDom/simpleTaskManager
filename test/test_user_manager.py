from typing import Type
import unittest
import logging
from unittest import mock
from src import user_manager

logger = logging.getLogger(__name__)

# Filename for mock file.
_MOCK_FILE_NAME_ = "test_user_manager"

# Hash function used by user_manager.
hash = user_manager.default_hasher #hash and verify

# Mock user data.
DATA_EXAMPLE = {
    user_manager.USER_LABELS[0]:'user',
    user_manager.USER_LABELS[1]:hash.hash('passw'),
    'bad label':'unused value'
}

# Mock file handler.
mock_handler = mock.Mock()

class TestOptionsMenu(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        
        filename = _MOCK_FILE_NAME_
        self.manager = user_manager.UserManager(
            filename=filename,
            file_handler=lambda *args, **kwargs: mock_handler) #type: ignore

    def setUp(self) -> None:
        global mock_handler
        mock_handler.buffer = [DATA_EXAMPLE]
        # 'Logout'
        self.manager._user = None
        return super().setUp()
    
    def tearDown(self) -> None:
        mock_handler.reset_mock()
        return super().tearDown()

##############################################
#                                            #
#           CALL FROM OPTIONS                #
#                                            #
##############################################

    def test_get_users_pwd(self):
        '''
           Test 'private' method _get_users_pwd.
        '''
        
        logging.info('test_get_users_pwd')

        pwd_by_name = self.manager._get_users_pwd
        self.assertTrue( hash.verify('passw', pwd_by_name['user']) )

    def test_user_exists(self):
        '''
           Test if user exists.
        '''

        logging.info('test_user_exists')

        self.assertTrue(self.manager.user_exists('user'))
        mock_handler.load.assert_called_once()

    def test_user_exists_not(self):
        '''
           Test if user does not exist.
        '''

        logging.info('test_user_exists_not')

        self.assertFalse(self.manager.user_exists('Douglas Adams'))
        mock_handler.load.assert_called_once()
          
    def test_add_user(self):
        '''
           Test adding a user.
        '''

        logging.info('test_add_user')

        self.manager.add_user('newUser', 'newPassword')
        self.assertTrue(hash.verify(
            'newPassword',
            mock_handler.buffer[-1][user_manager.USER_LABELS[1]]))

    def test_add_existing_user(self):
        '''
           Test adding an existing user.
        '''

        logging.info('test_add_existing_user')

        self.assertFalse(self.manager.add_user('user', 'newPassword'))

    def test_log_in(self):
        '''
           Test logging in.
        '''

        logging.info('test_log_in')

        self.assertTrue(self.manager.log_in('user', 'passw'))

    def test_log_in_fail(self):
        '''
           Test logging in with wrong password.
        '''

        logging.info('test_log_in_fail')

        self.assertFalse(self.manager.log_in('user', 'nope'))

    def test_log_in_and_out(self):
        '''
           Test logging in and out.
        '''

        logging.info('test_log_in_and_out')

        self.manager.log_in('user', 'passw')
        self.assertTrue(self.manager.user_logged)
        self.manager.log_in('user', 'not the password')
        self.assertFalse(self.manager.user_logged)

    def test_user_logged(self):
        '''
           Test logged user property.
        '''

        logging.info('test_user_logged')

        # Assert user not logged.
        self.assertFalse(self.manager.user_logged)
        self.manager.log_in('user', 'passw')
        # Assert user logged.
        self.assertTrue(self.manager.user_logged)

    @mock.patch('src.user_manager.data_file', lambda x: mock_handler)
    def test_is_admin(self):
        '''
           Test if logged user is admin.

           Use user file to read admin, guaranteeing user is admin.
        '''

        logging.info('test_is_admin')

        # Assert login did not fail
        self.assertTrue(self.manager.log_in('user', 'passw'))
        # Assert is_admin is True
        self.assertTrue(self.manager.is_admin)
    
    @mock.patch('src.user_manager.data_file', lambda x: mock_handler)
    def test_is_not_admin(self):
        '''
           Test if logged user is not admin.
        '''

        logging.info('test_is_not_admin')

        # Force fake user login
        self.manager._user = 'Douglas Adams'
        # Assert is_admin is False
        self.assertFalse(self.manager.is_admin)

    def test_users(self):
        '''
           Test users property.
        '''

        logging.info('test_users')
           
        users_iter = self.manager.users
        # Must return an iterator.
        self.assertIsNotNone(users_iter)
        # Which has one element with 'user'.
        user = next(users_iter)
        self.assertEqual(user, 'user')
        # And no more than one element.
        self.assertRaises(StopIteration, lambda:next(users_iter))