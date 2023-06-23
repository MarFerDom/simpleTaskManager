import os
import sys
import logging
from typing import List
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View():
    """
       LoginPrompt class for the application
    """
        
    def __init__(self, prompt: str = 'Prompt',
                 options: List[str] = ['exit'],
                 *args, **kwargs) -> None:
        '''
           Initializes the OptionsMenu.
        '''
        
        super().__init__(*args, **kwargs)
        self.prompt = prompt
        self.options = options
        self.controller_service = self.noActions

        logger.info(
            f'{self.__class__} presented user with {len(self.options)} options'
            )

    def refresh_screen(self):
        '''
           Refreshes screen for windows and linux.
        '''
        if sys.platform == 'win32' or 'cygwin':
            os.system('cls')
        else:
            os.system('clear')

    def bind_provider(self, call: protocols.ControllerSelect) -> None:
        '''
           Binds the function to the method
        '''

        logger.info(f'{self.__class__} binded to\
                     selection method {call.__name__}')
        self.controller_service = call
     
    def noActions(self, *args, **kwargs) -> None:
        logger.info(f'{self.__class__} tried to run but no method binded')
        print("No method binded")
    
    def mainloop(self):
        '''
           Prints options and returns user input.
        '''

        logger.info(f'{self.__class__} running.')
        # Refreshes screen.
        self.refresh_screen()
        
        # Prompts user for choice of option.
        header = ['',self.prompt]
        choice = input('\n'.join(header+self.options)+'\n').lower()

        # Finds option that matches user input earlier and select it.
        index = filter(
            lambda x: x[0] >= 0,
            [(opt.lower().find(choice), i) for i, opt in enumerate(self.options)]
            )
        try:
            index = min(index)[1]
        except ValueError:
            index = -1
        # Calls controller to select option.
        self.controller_service(index)
        logger.info(f'{self.__class__} closing.')
        
if __name__  == '__main__':
    options = ['Option 1', 'Option 2', 'Option 3']
    menu = View(options=options)
    menu.bind_provider(lambda x: print(f'Selected option {options[x]}'))
    menu.mainloop()