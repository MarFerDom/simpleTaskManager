import os
import sys
import logging
from getpass import getpass
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View():
    """
       Insert prompt class for the application.

       Used to request new owner or due date from the user.
    """
        
    def __init__(self,
                 prompt: str = "Enter new value",
                 success_msg: str = "Change Successful",
                 failure_msg: str = 'Change Failed',
                 input_list: list = ['new owner'],
                 *args, **kwargs) -> None:
        '''
           Initializes the Insert prompt
        '''
        
        super().__init__(*args, **kwargs)
        self.prompt = prompt
        self.success_msg = success_msg
        self.failure_msg = failure_msg
        self.input_list = input_list
        self.controller_service = self.noActions

    def refresh_screen(self):
        '''
           Refreshes screen for windows and linux.
        '''
        if sys.platform == 'win32' or 'cygwin':
            os.system('cls')
        else:
            os.system('clear')

    def bind_provider(self, call: protocols.ControllerInsert) -> None:
        '''
           Binds the service provider.
        '''
        
        logger.info(f'{self.__class__} binded to login method {call.__name__}')
        self.controller_service = call

    def noActions(self, *args, **kwargs) -> bool:
        logger.info(f'{self.__class__} tried to run but no method binded')
        print("No method binded")
        return False

    def mainloop(self):
        self.refresh_screen()
        # - Request new value.
        new_value = []
        for entry in self.input_list:
            new_value.append(input('\nEnter '+entry+'\n>'))
        try:
            if self.controller_service(new_value):
                logger.info(f'{self.prompt} successful for user {new_value}')
                input(self.success_msg)
            else:
                logger.info(f'{self.prompt} failed for user {new_value}')
                input(self.failure_msg)
        except protocols.ControllerError as e:
            input(e.args[0])

if __name__  == '__main__':
    View().mainloop()