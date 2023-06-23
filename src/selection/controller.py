import logging
from typing import List, Optional, Type
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

# Alias for the class type for the menu controller protocol.
UI_Class = Type[protocols.selection_controller_interface]

# Default prompt text for menu.
_DEFAULT_PROMPT_ = 'Select one of the following options below:'

class Controller():
    '''
       Class that controls option selection operations.
    '''
        
    def __init__(self,
                 user: protocols.user_protocol,
                 model: protocols.model_protocol,
                 view: Optional[UI_Class] = None,
                 prompt: str = _DEFAULT_PROMPT_,
                 success_msg: str = 'Option selected',
                 failure_msg: str = 'Invalid option',
                 id: int = -1,
                 next: str = 'Null',
                 source: str = 'user',
                 options: List[str] = ['exit'],
                 is_task: bool = False,
                 *args, **kwargs) -> None:
        '''
           Initializes the controller.
        '''

        # Easy binding
        self.model = model
        self.view = view
        # Prompt and messages.
        self.prompt = prompt
        self.success_msg = success_msg
        self.failure_msg = failure_msg
        # Data retriving.
        self.id = id
        self.next = next
        self.is_task = is_task

        # Set options available
        if source == 'user':
            # Get options list and mapping to real indices.
            self.options, self.mapping = model.get_all_tasks(user.user_logged)
            # For each option, add numbering for user selection.
            number_of_lines = len(self.options)
            number_of_digits = len(str(number_of_lines))
            for i in range(number_of_lines):
                self.options[i] = \
                    f'{i+1:0{number_of_digits}} - '.ljust(number_of_digits+3) \
                        + self.options[i]
        else:   
            self.options = options.copy()
        
        super().__init__()
    
    ##########################################
    #                                        #
    #   Bind                                 #
    #                                        #
    ##########################################

    def bind_UI(self, view: UI_Class):
        '''
            Binds the to the UI class.
        '''

        logger.info(f'{self.__class__} binded to class {view.__name__}')
        self.view = view

    ##########################################
    #                                        #
    #   Options Menu                         #
    #                                        #
    ##########################################
        
    def select(self, index: int):
        '''
            Sets the action at index for next stage.
        '''
        
        # If in view mine mode:
        #   - Next only changes if -1 entered.
        #   - id is defined by the option or -1.
        if hasattr(self,'mapping'):
            if index == -1:
                self.next = "main menu"
                self.id = -1
                return
            self.id = self.mapping[index]
            return
        
        # If in edit task or main menu:
        #   - Next is defined by the option.
        self.next = self.options[index]
    
    ##########################################
    #                                        #
    #   Run                                  #
    #                                        #
    ##########################################

    def run(self):
        '''
            Runs the options menu.
        '''
        
        logger.info(f'{self.__class__} running.')

        # Raise error if UI not binded.
        if self.view is None:
            raise protocols.ControllerError("No UI binded")
        
        if self.is_task:
            # Create a header for the current task data
            header = self.model.get_task(self.id)
            header = header + '\n'*2
            self.prompt = header + self.prompt
        # Create the view
        view = self.view(prompt=self.prompt, options=self.options)
        # Bind options and selection method to view.
        view.bind_provider(self.select)
        # Run view.
        view.mainloop()
        logger.info(f'{self.__class__} closing.')

if  __name__ == "__main__":
    print(f'{__file__}: This module cannot be run directly.')

    # menu = OptionsMenu(actions=[{'text':'exit', 'action': lambda: None}])
    # menu.bind_UI(selection_view)
    # menu.run()