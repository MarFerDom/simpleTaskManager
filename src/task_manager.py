import json
import importlib
import logging
import time

from functools import partial
from typing import Type

from src import protocols, config, user_manager
from src.task_master import local_model

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)
# Set default view type as prompt.
DEFAULT_VIEW = '.prompt'

# States are methods that return the next state when called
#   Arguments:
#    user: user_protocol
#    model: model_protocol
#    id: id of the task being processed if any.


# State list information is loaded from the configuration file.
with open(config._APP_STATE_CONFIG_) as f:
    config_data = json.load(f)
    # Get start state.
    START_STATE = config_data['start_state']
    # Filter states missing name and name of type.
    STATE_DATA = list(filter(
        lambda x:('name_of_type' in x.keys() and 'name' in x.keys()),
        config_data['states']
        ))
    
# Check for valid states.
assert len(STATE_DATA) > 0, 'App has no states'
# Check for valid start state.
assert START_STATE in [state['name'] for state in STATE_DATA], 'Initial state is not valid'

# Creates a state preconfigured to specific task.
def get_state(**kwargs):
    '''
       Loads module if necessary and returns the state with configurations set.
    '''

    # If no name of type is given, return None.
    if kwargs.get('name_of_type', 'Null') == 'Null':
        return None, None
    # Copy args to avoid changing them.
    args_ = kwargs.copy()

    # Get type of State to configure.
    module = 'src.' + args_['name_of_type'] + '.controller'
    
    # Get view for state.
    view_type = 'src.' + args_['name_of_type'] + DEFAULT_VIEW

    # Loads module and view. Defaults to 'exit' if fail.
    # Load module if necessary.
    if module not in globals():
        try:
            globals()[module] = importlib.import_module(module)
        except:
            logger.error(f"Could not load module {module}")
            return None, None
    # Load view if necessary.
    if view_type not in globals():
        try:
            globals()[view_type] = importlib.import_module(view_type)
        except:
            logger.error(f"Could not load view {view_type}")
            return None, None
        
    # Return configured state.
    return (partial(globals()[module].Controller, **args_),
            globals()[view_type].View)


# Main class that controls the application. 
class TaskManager():
    '''
       Class that controls the applcation state transitions.
    '''

    def __new__(cls,
                 user: protocols.user_protocol,
                 model: protocols.model_protocol,
                 start: str = 'Null') -> 'TaskManager':
        '''
           Guarantees only one instance of the class is created.
        '''

        if not hasattr(cls, 'instance'):
            cls.instance = super(TaskManager, cls).__new__(cls)
            cls.instance.is_set = False
        return cls.instance
    
    def __init__(self,
                 user: protocols.user_protocol,
                 model: protocols.model_protocol,
                 start: str = 'Null') -> None:
        super().__init__()

        # Avoid changes in case of existing instance.
        if self.is_set: return
        # Set user manager and data model.
        self.user = user
        self.model = model
        # Defines current state of app.
        self.state = start
        # Defines restaring state after crashes.
        self.restart_state = start
        # Set initialization flag to true.
        self.is_set = True
        # Keep an index of the current task being processed.
        self.task_index = -1

    def state_wrapper(self, pre_controller: Type[protocols.preconfigured_controller]):
        '''
           Wraps Controller class as a callable
        '''

        def wrapper(user:protocols.user_protocol, model:protocols.model_protocol):
            # Create controller and bind view.
            state = pre_controller(user=user, model=model, id=self.task_index)
            state.bind_UI(view=self.current_view)
            # Run and store new id.
            state.run()
            self.task_index = state.id
            # Returns the next state of the program.
            return state.next
        return wrapper

    def run(self) -> None:
        '''
           Runs current state and sets next until type of state is 'Null'.
        '''

        while True:
            logger.info(f'State to run: {self.state}')
            # State configuration.
            try:
                # Find state configuration.
                state_config = next(
                    filter(
                        lambda x: x['name'] == self.state,
                        STATE_DATA
                    )
                )
            except StopIteration:
                # Or set to null is not found.
                state_config = {'name of type': 'Null'}

            logger.info(f'next_state: {state_config}')
            # Get state to execute and .
            next_state, self.current_view = get_state(**state_config)
            logger.info(f'next_state: {next_state}')

            # Check for end of app.
            if next_state is None: break

            # Run to next state.
            try:
                # Create callable state.
                callable_state = self.state_wrapper(next_state) #type: ignore
                # Execute state.
                self.state = callable_state(self.user, self.model) 
            except ValueError as e:
                # Print error message and restart.
                print(f'{self.__class__.__name__} crashed with call to:',
                      f'\t-> {self.state}(' + \
                        f'{self.user.__class__}, ' + \
                        f'{self.model.__class__})',
                      f'\traised: <ValueError: {e.args[0]}>\n', sep='\n')
                logger.error(e)

                # Set state to restart state.
                self.state = self.restart_state
                # Give 4 seconds for the user to read.
                simb = r'/|\-'
                for i in range(len(simb)*2):
                    print(f'restarting...{simb[i%len(simb)]}', end='\r')
                    # wait for half a second.
                    time.sleep(0.5)     

        # Save changes to tasks.
        self.model.save_tasks()
        # Clear instance reference from class.
        TaskManager._kill()
            
    @classmethod
    def _kill(cls) -> None:
        '''
           Kills the current instance of the class.
        '''

        del cls.instance

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description = 'Example of {} module'.format(__file__.split("\\")[-1]))
    parser.add_argument('--UI', type=str,
                        help='UI to use: prompt or view')
    args = parser.parse_args()

    UI_options = ['prompt', 'GUI']
    if args.UI is not None:
        if args.UI in UI_options:
            DEFAULT_VIEW = '.'+args.UI
        else:
            parser.error(f'Invalid UI option: {args.UI}')
            
    # Create task manager
    app = TaskManager(
        user=user_manager.UserManager(),
        model=local_model.Model(),
        start=START_STATE)
    app.run()