import logging
import logging.handlers

######################
# SYSYEM FILES PATHS #
######################

# File that contains app state:
# - App states configuration.
_APP_STATE_CONFIG_ = 'app/app_config.json'

# File that contains list of ADMIN users:
# - Separated by newlines, semicolons or a mix.
_ADMIN_FILE_ = 'etc/.ADMIN'


# File that contains list of USER and PASSWORDS:
# - Each pair as semicolons separated values.
_USER_FILE_ = 'etc/.USER'

# File that contains list of tasks:
# - Each task as semicolon separated values.
_TASK_FILE_ = 'etc/.TASK'

# User report file:
# - Human readable file.
_USER_REPORT_FILE_ = 'reports/USER_REPORT'

# Task report file:
# - Human readable file.
_TASK_REPORT_FILE_ = 'reports/TASK_REPORT'

# Path to ENV file.
_ENV_PATH_ = '.env'


# Path to dummy file for test purposes:
# - Used as default value for file path.
_DUMMY_FILE_ = "dummy.txt"


# Path to LOG file.
_LOG_FILE_ = 'etc/.LOG'


#######################
# LOGGING ROOT CONFIG #
#######################

# Logging basic config 
# logging.basicConfig(filename=_LOG_FILE_,
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.INFO)
logging.getLogger('').setLevel(logging.NOTSET)
rotatingHandler = logging.handlers.RotatingFileHandler(
    filename=_LOG_FILE_, maxBytes=10_000, backupCount=5)
rotatingHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotatingHandler.setFormatter(formatter)
logging.getLogger('').addHandler(rotatingHandler)


######################
# MODULES TO PLUG IN #
######################

LOGIN_INTERFACE='src.login_view.Login'
SELECTION_INTERFACE='src.selection_prompt.OptionsMenu'
PRESENTATION_INTERFACE='src.presentation_prompt.Presentation'
INSERTION_INTERFACE='src.insert_prompt.Insert'

PASSWORD_HASHER='passlib.hash.pbkdf2_sha256'
FILE_HANDLER='src.file_handler.SCSVFileHandler'
REPORT_HANDLER='src.file_handler.ReportFileHandler'
USER_MANAGER='src.user_manager.UserManager'