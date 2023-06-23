from typing import Any, Iterator, Mapping, Optional, Protocol, Callable, List, Tuple, Type

class ControllerError(ValueError):
    pass

####################
# Method Signature #
####################

ControllerSelect = Callable[[int], None]
ControllerInsert = Callable[[List[str]], bool]
ControllerPresent = Callable[[], str]
ControllerUserService = Callable[..., bool]

##################
# Data protocols #
##################

class user_protocol(Protocol):
    def user_exists(self, user:str, *args, **kwargs) -> bool:
        ...
    def add_user(self, user:str, pwd:str) -> bool:
        ...
    def log_in(self, user:str, pwd:str) -> bool:
        ...
    @property
    def user_logged(self) -> Optional[str]:
        ...  
    @property
    def is_admin(self) -> bool:
        ...
    @property
    def users(self) -> Iterator[str]:
        ...
    def __len__(self) -> int:
        ...

class model_protocol(Protocol):
    def get_all_tasks(self,
                      user: Optional[str] = None) -> Tuple[List[str], List[int]]:
        ...
    def get_task(self, index: int) -> Any:
        ...
    def add_task(self, data: List[str]) -> bool:
        ...
    def mark_as_completed(self, task_id:int) -> None:
        ...
    def is_task_completed(self, task_id:int) -> bool:
        ...
    def edit_user(self, task_id:int, owner:str) -> bool:
        ...
    def edit_date(self, task_id:int, date:str) -> bool:
        ...
    def save_tasks(self):
        ...
    def read_report(self, userlist: List[str]) -> str:
        ...
    def write_report(self, userlist: List[str]) -> None:
        ...

State = Callable[[user_protocol, model_protocol, int, str], Any]

Actions = List[Mapping[str, Any]]

################
# UI protocols #
################

class user_controller_interface(Protocol):
    '''
       Protocol for login UI.
    '''

    def __init__(self,
                 prompt: str = "LOGIN",
                 success_msg: str = "Login Successful",
                 failure_msg: str = 'Login Failed',
                 operation: str = 'login',
                 *args, **kwargs) -> None:
        ...
    def bind_provider(self, call: ControllerUserService) -> None:
        ...
    def mainloop(self):
        ...

class selection_controller_interface(Protocol):
    '''
       Protocol for menu UI.
    '''

    def __init__(self, prompt: str = 'Prompt',
                 options: List[str] = ['exit'],
                 *args, **kwargs) -> None:
        ...
    def bind_provider(self, call:ControllerSelect) -> None:
        ...
    def mainloop(self):
        ...

class insert_controller_interface(Protocol):
    '''
       Protocol for insertion UI.
    '''

    def __init__(self,
                 prompt: str = "Enter new value",
                 success_msg: str = "Change Successful",
                 failure_msg: str = 'Change Failed',
                 input_list: list = ['new owner'],
                 *args, **kwargs) -> None:
        ...
    def bind_provider(self, call: ControllerInsert) -> None:
        ...
    def mainloop(self):
        ...

class presentation_controller_interface(Protocol):
    '''
       Protocol for presentation UI.
    '''

    def __init__(self, prompt:str) -> None:
        ...
    def bind_provider(self, call:ControllerPresent) -> None:
        ...
    def mainloop(self):
        ...

########################
# Controller protocols #
########################

class preconfigured_controller(Protocol):
    '''
       Protocol for preconfigured controller to be initialized.
    '''

    def __init__(self,
                 user: user_protocol,
                 model: model_protocol,
                 id: int = -1,
                 *args, **kwargs) -> None:
        ... 
    def bind_UI(self, view):
        ...
    def run(self) -> None:
        ...
    id:int
    next:str

class user_operations_controller(Protocol):
    '''
       Protocol for subcontroller that runs a login.
    '''

    def bind_UI(self, view: Type[user_controller_interface]):
        ...
    def bind_provider(self, provider: user_protocol):
        ...
    def controller_service(self, user: str, password: str,
                           repeat_pass: str = '') -> bool:
        ...
    def run(self) -> None:
        ...

class menu_controller(Protocol):
    '''
       Protocol for subcontroller that runs a menu.
    '''

    def bind_UI(self, view: Type[selection_controller_interface]):
        ...
    def add_actions(self, actions: Actions) -> None:
        ...
    def run(self) -> None:
        ...

class insert_controller(Protocol):
    '''
       Protocol for subcontroller that runs a menu.
    '''

    def bind_UI(self, view: Type[insert_controller_interface]):
        ...
    def bind_provider(self, provider: ControllerInsert):
        ...
    def run(self) -> None:
        ...

class present_controller(Protocol):
    '''
       Protocol for subcontroller that runs a menu.
    '''

    def bind_UI(self, view: Type[presentation_controller_interface]):
        ...
    def bind_provider(self, provider: ControllerPresent):
        ...
    def run(self) -> None:
        ...

if __name__ == '__main__':
    print(f'{__file__.split("/")[-1]}: This module cannot be run directly.')