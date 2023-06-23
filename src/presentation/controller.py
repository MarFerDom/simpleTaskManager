import logging
from typing import List, Optional, Type
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

# Alias for the class type for the presentation controller protocol.
UI_Class = Type[protocols.presentation_controller_interface]

# Default prompt text for menu.
_DEFAULT_TITLE_ = 'All tasks'
_DEFAULT_OP_ = 'view all'

class Controller():
    '''
       Class that controls presentation.
    '''
        
    def __init__(self,
                 user: protocols.user_protocol,
                 model: protocols.model_protocol,
                 view: Optional[UI_Class] = None,
                 prompt: str = _DEFAULT_TITLE_,
                 id: int = -1,
                 next: str = 'Null',
                 operation: str = _DEFAULT_OP_,
                 *args, **kwargs) -> None:
        '''
           Initializes the controller.
        '''

        # Prompt text.
        self.prompt = prompt
        # Easy binding
        self.user = user
        self.model = model
        self.view = view
        self.operation = operation
        self.id = id
        self.next = next
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
    
    # Controller in the middle
    def controller_service(self, *args, **kwargs) -> str:
        '''
           Controller connects the view and the model
           and provides flow control and data validation.
        '''

        if self.operation == _DEFAULT_OP_:
            out = '\n'.join(self.model.get_all_tasks()[0])
        else:
            if self.user.is_admin:
                out = self.model.read_report(list(self.user.users))
            else:
                out = 'Access denied: Admin only'
        # Do something with out
        return out
    
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
            raise protocols.ControllerError("No presenter UI binded")
        
        # Change prompt for display statistics
        if self.operation != _DEFAULT_OP_: self.prompt = 'Return'
        # Create the view
        view = self.view(prompt=self.prompt)
        # Bind presentation method to view.
        view.bind_provider(self.controller_service)
        # Run view.
        view.mainloop()

        # Reset id at the end for next state.
        self.id = -1
        logger.info(f'{self.__class__} closing.')

if  __name__ == "__main__":
    print(f'{__file__}: This module cannot be run directly.')