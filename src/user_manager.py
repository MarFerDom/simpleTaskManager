import logging
from src import file_handler, plugin, config
from typing import Iterator, Optional, Type

default_hasher = plugin.get_class(config.PASSWORD_HASHER)
data_file = plugin.get_class(config.FILE_HANDLER)

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

USER_LABELS = ['username', 'password']

class UserError(ValueError):
    '''
       Error raised when user operation is invalid.
    '''
    ...

class UserManager():
    '''
       Class for managing users.

       Deals with login and keeps hashed passwords.
       Defaults to SCSVFileHandler with default file path.
    '''    

    def __init__(self,
                 filename: str = config._USER_FILE_,
                 file_handler: Type[file_handler.FileHandler] \
                                = file_handler.SCSVFileHandler,
                 *args, **kwargs):
        super(UserManager, self).__init__(*args, **kwargs)
        self._file = file_handler(filename, labels=USER_LABELS)
        self._user: Optional[str] = None

    @property
    def _get_users_pwd(self) -> file_handler.DATA_TYPE:
        '''
           Reads 'username' and 'password' [USER_LABELS] from file handler
           and returns as a dictionary.
        '''

        logger.info(f'Reading {USER_LABELS[0]} and'+\
                     f'{USER_LABELS[1]} from {self._file}')
        self._file.load()
        return {data[USER_LABELS[0]]:data[USER_LABELS[1]]
                for data in self._file.buffer}
    
    def user_exists(self, user:str, *args, **kwargs) -> bool:
        '''
           Checks if username already exists
        '''

        return user in self._get_users_pwd.keys()
    
    def add_user(self, user:str, pwd:str) -> bool:
        '''
           Call write on file handler passing username and password
           as a one item list of dictionaries using USER_LABELS.
        '''

        if user == '' or pwd == '': return False
        if self.user_exists(user): return False
                            #raise UserError('User already exists.')
        self._file.buffer.append({
            USER_LABELS[0]:user,
            USER_LABELS[1]:default_hasher.hash(pwd)})
        self._file.dump()
        return True
    
    def log_in(self, user:str, pwd:str) -> bool:
        '''
           Logs in if matching username and password.
        '''
        if self._user is not None:
            logging.info(f'Logged out of {self._user}')
            self._user = None
        
        try:
            if  default_hasher.verify(pwd,
                                  self._get_users_pwd.get(user, '')):
                self._user = user
                return True
        except:
            pass
        
        return False
    
    @property
    def user_logged(self) -> Optional[str]:
        '''
           Returns logged in username.
        '''

        return self._user

    @property
    def is_admin(self) -> bool:
        '''
           Returns True if logged user is part of 'admin' list.
        '''

        # Get list of admin users from '.ADMIN' file.
        admin_list = data_file(config._ADMIN_FILE_)
        admin_list.load()
        # Admin file has on labels, every admin name is a value.
        return any([self._user in admin_dic.values() for admin_dic in admin_list.buffer])
    
    @property
    def users(self) -> Iterator[str]:
        '''
           Iterator of usernames.
        '''

        return iter(self._get_users_pwd.keys())
    
    def __len__(self) -> int:
        return len(self._get_users_pwd)
    

if __name__ == '__main__':

    manager = UserManager()
    #manager.add_user('tester', 'testing')
    manager.log_in('admin', 'admin')
    print(manager.user_logged)