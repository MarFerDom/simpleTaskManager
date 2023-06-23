import logging
from typing import Optional, Type
from src import protocols
from src.task_master import single_task

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

# Alias for the class type for the insertion controller protocol.
UI_Class = Type[protocols.insert_controller_interface]

# Default prompt text for menu.
_DEFAULT_PROMPT_ = 'Change tasks owner'
_OPERATIONS_ = ['edit user', 'edit date', 'add task']

ESCAPE_STATE = 'main menu'

class Controller():
    '''
       Class that controls presentation.
    '''
        
    def __init__(self,
                 model: Optional[protocols.model_protocol] = None,
                 view: Optional[UI_Class] = None,
                 prompt: str = _DEFAULT_PROMPT_,
                 success_msg: str = 'Edit successfully',
                 failure_msg: str = 'Edit failed',
                 operation: str = _OPERATIONS_[0],
                 id: int = -1,
                 next: str = 'Null',
                 *args, **kwargs) -> None:
        '''
           Initializes the controller.
        '''

        # Easy binding
        self.provider = model
        self.view = view

        # Prompt text.
        self.prompt = prompt
        self.success_msg = success_msg
        self.failure_msg = failure_msg
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

    def bind_provider(self, provider: protocols.model_protocol) -> None:
        '''
            Binds to the provider.
        '''

        logger.info(f'{self.__class__} binded to class {provider.__class__}')
        self.provider = provider
    
    # Controller in the middle
    def controller_service(self, user_input: list) -> bool:
        '''
           Controller connects the view and the model
           and provides flow control and data validation.
        '''

        if self.provider is None: return False
        
        entries = [entry.strip() for entry in user_input]
        out = False
        if self.operation == _OPERATIONS_[0]:
            if len(entries) != 1:
                raise protocols.ControllerError('Edit user: wrong list of arguments')
            if self.provider.is_task_completed(self.id):
                raise protocols.ControllerError('Can not edit. Task already completed')
            try:
                out = self.provider.edit_user(task_id=self.id, owner=entries[0])
            except:
                raise protocols.ControllerError('Invalid user name')

        if self.operation == _OPERATIONS_[1]:
            if len(entries) != 1:
                raise protocols.ControllerError('Edit date: wrong list of arguments')
            if self.provider.is_task_completed(self.id):
                raise protocols.ControllerError('Can not edit. Task already completed')
            try:
                out = self.provider.edit_date(task_id=self.id, date=entries[0])
            except:
                raise protocols.ControllerError('Invalid date format')

        if self.operation == _OPERATIONS_[2]:
            
            # Owner may not be empty
            if not len(entries[0]): raise protocols.ControllerError("Empty username not allowed")
            # Title may not be empty
            if not len(entries[1]): raise protocols.ControllerError("Empty title not allowed")
            try:
                out = self.provider.add_task(data=entries)
            except:
                raise protocols.ControllerError('Invalid task format')

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
        # Raise error if provider not binded.
        if self.provider is None:
            raise protocols.ControllerError("No presenter provider binded")
        
        # Select the appropriate input list.
        input_list = []
        if self.operation == _OPERATIONS_[0]:
            input_list = ['new owner']
            self.prompt = 'Enter new task owner\'s name'
        if self.operation == _OPERATIONS_[1]:
            input_list = ['new due date']
            self.prompt = 'Enter new due date'
        if self.operation == _OPERATIONS_[2]:
            input_list = single_task.TASK_LABELS
            self.prompt = 'Enter new task'
            self.success_msg = 'Created new task'
            self.failure_msg = 'Task creation failed'

        # Create the view.
        view = self.view(
            prompt=self.prompt,
            success_msg=self.success_msg,
            failure_msg=self.failure_msg,
            input_list=input_list
        )
    
        # Bind presentation method to view.
        view.bind_provider(self.controller_service)
        # Run view.
        view.mainloop()
        
        # Reset id at the end for next state.
        self.id = -1
        self.next = ESCAPE_STATE
        logger.info(f'{self.__class__} closing.')

if  __name__ == "__main__":
    print(f'{__file__}: This module cannot be run directly.')

    # menu = OptionsMenu(actions=[{'text':'exit', 'action': lambda: None}])
    # menu.bind_UI(selection_view)
    # menu.run()