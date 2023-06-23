import logging
from typing import Optional, Type
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

UI_Class = Type[protocols.user_controller_interface]

class Controller():
    '''
       Class that controls user operations.
    '''
        
    def __init__(self,
                 user: Optional[protocols.user_protocol] = None,
                 view: Optional[UI_Class] = None,
                 prompt: str = "Login",
                 success_msg: str = "Login Successful",
                 failure_msg: str = 'Login Failed',
                 operation: str = 'login',
                 id: int = -1,
                 next: str = 'Null',
                 *args, **kwargs) -> None:
        '''
           Initializes the controller.
        '''

        # Easy binding
        self.user = user
        self.view = view
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
            Binds to the UI class.
        '''

        logger.info(f'{self.__class__} binded to class {view.__name__}')
        self.view = view
    
    def bind_provider(self, user: protocols.user_protocol) -> None:
        '''
            Binds to the provider.
        '''

        logger.info(f'{self.__class__} binded to class {user.__class__}')
        self.user = user

    # Controller in the middle
    def controller_service(self, user: str, password: str,
                           repeat_pass: str = '') -> bool:
        '''
           Controller connects the view and the model
           and provides flow control and data validation.
        '''

        # Raise error if user management provider not binded.
        if self.user is None:
            raise protocols.ControllerError("404 - Request not found")
        
        out = False
        # Login operation.
        if self.operation == 'login':
            # Use empty username and password as an exit option.
            if user == '' and password == '':
                logger.info("Exited with empty user and password")
                self.next = 'Null'
                raise protocols.ControllerError("\n\nExiting.. press enter to quit")
            out = self.user.log_in(user, password) #type: ignore

        # Register operation: validate password first.
        if self.operation =='register':
            if self.user.user_exists(user): raise protocols.ControllerError("User already exists")
            if user == '': raise protocols.ControllerError("Usename cannot be empty")
            if password == '': raise protocols.ControllerError("Password cannot be empty")
            if repeat_pass != password: raise protocols.ControllerError("Passwords do not match")
            out = self.user.add_user(user, password) #type: ignore
        
        return out
    
    ##########################################
    #                                        #
    #   Run                                  #
    #                                        #
    ##########################################

    def run(self):
        '''
            Runs the login.
        '''
        
        logger.info(f'{self.__class__} running.')

        # Raise error if UI not binded.
        if self.view is None:
            raise protocols.ControllerError("No UI binded")
        # Raise error if user management provider not binded.
        if self.user is None:
            raise protocols.ControllerError("No service provider binded")
        
        # Create the view
        view = self.view(prompt=self.prompt, success_msg=self.success_msg,
                         failure_msg=self.failure_msg, operation=self.operation)
        # Bind options and selection method to view.
        view.bind_provider(self.controller_service)

        # Run view.
        view.mainloop()
        
        # Reset id at the end for next state.
        self.id = -1
        logger.info(f'{self.__class__} closing.')

if  __name__ == "__main__":
    print(f'{__file__}: This module cannot be run directly.')