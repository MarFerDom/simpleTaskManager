import os
import sys
import logging
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View():
    """
       Presentation class for the application.
    """
        
    def __init__(self, prompt: str = 'Press enter to return to main menu.',
                 *args, **kwargs) -> None:
        '''
           Initializes the OptionsMenu.
        '''
        
        super().__init__(*args, **kwargs)
        self.prompt = prompt
        self.controller_service = self.noActions

    def refresh_screen(self):
        '''
           Refreshes screen for windows and linux.
        '''
        if sys.platform == 'win32' or 'cygwin':
            os.system('cls')
        else:
            os.system('clear')

    def bind_provider(self, call: protocols.ControllerPresent) -> None:
        '''
           Binds the service provider.
        '''

        logger.info(f'{self.__class__} binded to\
                     selection method {call.__name__}')
        self.controller_service = call
     
    def noActions(self, *args, **kwargs) -> str:
        logger.info(f'{self.__class__} tried to run but no method binded')
        print("No method binded")
        return ''
    
    def mainloop(self):
        '''
           Prints options and returns user input.
        '''

        logger.info(f'{self.__class__} running.')
        # Refreshes screen.
        self.refresh_screen()
        
        # Prompts user for choice of option.
        print()
        input(self.controller_service() + '\n\n' + self.prompt)

        logger.info(f'{self.__class__} closing.')
        
if __name__  == '__main__':
    menu = View()
    menu.bind_provider(lambda: f'This is a presentation')
    menu.mainloop()