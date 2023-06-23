import os
import sys
from typing import Protocol, List
from importlib import import_module
from dotenv import load_dotenv

from src import config

# Load environmental variables from .ENV file.
load_dotenv(config._ENV_PATH_)

# Append current 'src' directory to path.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Method to import class from string path.
def get_class(path: str):
    parts: List[str] = path.split('.')

    if len(parts) < 2:
        raise ValueError('Invalid class path')
    # Loads the module and returns the class.
    return getattr(import_module('.'.join(parts[:-1]), parts[0]), parts[-1])

# Load view for login operation
#login_view = get_class(config.LOGIN_INTERFACE)

# Load view for selection operation
#selection_view = get_class(config.SELECTION_INTERFACE)

# Load default password hasher class.
#default_hasher = get_class(config.PASSWORD_HASHER)

# Load file handler class for users and tasks files.
#data_file = get_class(config.FILE_HANDLER)

# Load file handler class for report files.
#report_file = get_class(config.REPORT_HANDLER)

# Load file handler class for report files.
#user_manager_class = get_class(config.USER_MANAGER)



# # Load view for login operation
# login_view = get_class(os.environ['LOGIN_INTERFACE'])
# # Load view for selection operation
# selection_view = get_class(os.environ['SELECTION_INTERFACE'])
# # Load default password hasher class.
# default_hasher = get_class(os.environ['PASSWORD_HASHER'])
# # Load file handler class for users and tasks files.
# data_file = get_class(os.environ['FILE_HANDLER'])
# # Load file handler class for report files.
# report_file = get_class(os.environ['REPORT_HANDLER'])









class pluginType(Protocol):
    '''
       Modules to be loaded require a register method
    '''
    def register(self) -> None:
        ...


def load_plugins(plugin_names: List[str]) -> None:
    '''
       Loads plugin modules into memory and register it.
    '''
    for plugin in plugin_names:
        module = import_module(plugin)
        module.register()

if __name__ == '__main__':
    
    print(f'{__file__.split("/")[-1]}: This module cannot be run directly.')