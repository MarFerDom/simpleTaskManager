import unittest
import logging
from unittest import mock
from src import protocols
from src.user_op import controller

logger = logging.getLogger(__name__)

class TestLogin(unittest.TestCase):
   '''
      Tests setting up and running a login controller.
   '''

   def setUp(self) -> None:
      '''
         Set up for every test.
      '''

      # Creates a new login controller every test.
      self.operation_controller = controller.Controller()

      # Creates mocks for the UI and the login provider.
      self.view = mock.Mock()
      self.user = mock.Mock()
      self.user.log_in.return_value = True
      self.user.add_user.return_value = True
      self.user.user_exists.return_value = False
      return super().setUp()

##############################################
#                                            #
#               Setting Up                   #
#                                            #
##############################################

   def test_no_login_provider(self):
      '''
         Test starting login with no provider binded.
      '''

      logging.info('test_no_login_provider')

      # Bind login UI.
      self.operation_controller.bind_UI(view=lambda **_:self.view) #type: ignore

      # Assert ControllerError raised due to lack of provider.
      self.assertRaises(protocols.ControllerError, self.operation_controller.run)

   def test_no_login_UI(self):
      '''
         Test starting login with no UI binded.
      '''

      logging.info('test_no_login_UI')

      # Bind login provider.
      self.operation_controller.bind_provider(user=self.user) 
      
      # Assert ControllerError raised due to lack of UI.
      self.assertRaises(protocols.ControllerError, self.operation_controller.run)

   def test_run(self):
      '''
         Test running.
      '''
      
      logging.info('test_run')
      
      # Bind login UI and provider.
      self.operation_controller.bind_UI(view=lambda **_:self.view) #type: ignore
      self.operation_controller.bind_provider(user=self.user)

      # Run login controller.        
      self.operation_controller.run()

      # Asserts bind_login called as predicted.
      self.view.bind_provider.assert_called_once()
      # Assert mainloop called as predicted.
      self.view.mainloop.assert_called_once()

##############################################
#                                            #
#              Login service                 #
#                                            #
##############################################

   def test_login_service(self):
      '''
         Test login service.
      '''
      
      logging.info('test_login_service')
        
      # Bind provider
      self.operation_controller.bind_provider(user=self.user)

      self.operation_controller.controller_service('user','password')
      
      # Asserts the write method was called.
      self.user.log_in.assert_called_once()
      self.user.add_user.assert_not_called()


##############################################
#                                            #
#            User registration               #
#                                            #
##############################################

   def test_register_user_password_mismatch(self):
      '''
         Test register service with mismatched passwords.
      '''
      
      logging.info('test_register_user_password_mismatch')
        
      # Creates a new login controller for this test.
      self.operation_controller = controller.Controller(operation='register')

      # Bind provider
      self.operation_controller.bind_provider(user=self.user)

      # Failing password validation.
      self.assertRaises(protocols.ControllerError,
         self.operation_controller.controller_service, 'user','password', '')
      
      # Asserts the write method was called.
      self.user.log_in.assert_not_called()
      self.user.add_user.assert_not_called()

   def test_register_user_password_confirm(self):
      '''
         Test register service with matched passwords.
      '''
      
      logging.info('test_register_user_password_confirm')
        
      # Creates a new login controller for this test.
      self.operation_controller = controller.Controller(operation='register')

      # Bind provider
      self.operation_controller.bind_provider(user=self.user)

      # Failing password validation.
      self.assertTrue(
         self.operation_controller.controller_service('user','pass', 'pass'))
      
      # Asserts the write method was called.
      self.user.log_in.assert_not_called()
      self.user.add_user.assert_called_once()

   def test_register_existing_user(self):
      '''
         Test register service with existing user.
      '''
      
      self.user.user_exists.return_value = True
      logging.info('test_register_existing_user')
        
      # Creates a new login controller for this test.
      self.operation_controller = controller.Controller(operation='register')

      # Bind provider
      self.operation_controller.bind_provider(user=self.user)

      # Failing password validation.
      self.assertRaises(protocols.ControllerError,
         self.operation_controller.controller_service, 'user','pass', 'pass')
      
      # Asserts the write method was called.
      self.user.log_in.assert_not_called()
      self.user.add_user.assert_not_called()
