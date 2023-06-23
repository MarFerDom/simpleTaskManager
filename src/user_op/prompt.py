import os
import sys
import logging
import warnings
from getpass import getpass
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View():
    """
       LoginPrompt class for the application.

       Used to request username and password from the user.
       Can be used to get new username password as well.
    """

    def __new__(cls,
                prompt: str = "LOGIN",
                success_msg: str = "Login Successful",
                failure_msg: str = 'Login Failed',
                operation: str = 'login',
                *args, **kwargs) -> 'View':
        '''
           Guarantees only one instance of the class is created
        '''
        logger.info(f'{cls.__name__}.__new__ called')
        if not hasattr(cls, 'instance'):
            cls.instance = super(View, cls).__new__(
                cls, *args, **kwargs)
            logger.info(f'{cls.__name__} created new instance')
        return cls.instance
        
    def __init__(self,
                 prompt: str = "LOGIN",
                 success_msg: str = "Login Successful",
                 failure_msg: str = 'Login Failed',
                 operation: str = 'login',
                 *args, **kwargs) -> None:
        '''
           Initializes the LoginPrompt
        '''
        super().__init__(*args, **kwargs)
        self.prompt = prompt
        self.success_msg = success_msg
        self.failure_msg = failure_msg
        self.operation = operation
        self.controller_service = self.noLogin

    def refresh_screen(self):
        '''
           Refreshes screen for windows and linux.
        '''
        if sys.platform == 'win32' or 'cygwin':
            os.system('cls')
        else:
            os.system('clear')

    def bind_provider(self, call: protocols.ControllerUserService) -> None:
        '''
           Binds the function to the method
        '''
        
        logger.info(f'{self.__class__} binded to login method {call.__name__}')
        self.controller_service = call
        
    def noLogin(self, *args, **kwargs) -> bool:
        warnings.warn("No method binded")
        self.loop = False
        return False

    def mainloop(self):
        self.loop = True
        while(self.loop):
            self.refresh_screen()
            # - Request username and password.
            print('',self.prompt,'', sep='\n')
            username, password = input("Username: "), getpass("Password: ")
            response = False
            try:
                if self.operation == 'login':
                    response = self.controller_service(username, password)
                
                if self.operation == 'register':
                    password2 = getpass("Confirm password: ")
                    response = self.controller_service(username, password, password2)
            except protocols.ControllerError as e:
                input(e.args[0])
                break

            if response:
                logger.info(f'{self.prompt} successful for user {username}')
                print(self.success_msg)
                break
            
            logger.info(f'{self.prompt} failed for user {username}')
            input(self.failure_msg)
            if self.operation == 'register': break

if __name__  == '__main__':
    View(operation='register').mainloop()