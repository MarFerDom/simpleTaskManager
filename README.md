# Simple Task Manager <a id="top"></a>

Simple Task Manger made during HyperionDev's bootcamp.

The exercise required the refactoring of an incomplete task manager and its conclusion. The application edits, stores and presents tasks and task owners following a set of requirements presented in [Project Requirements](#proj_req) Additionally unittest was used in a Test Driven Development (TDD), and more abstractions and dependency inversion was inserted to make it flexible to changes, as an extension to the original premise.

### Content in this file:
* [Requirements](#req)
* [Installation](#install)
* [Usage](#usage)
* [TODO](#todo)
* [Components](#comp)
    * [Application Configuration](#app_conf)
    * [Model](#model)
    * [States](#states)
    * [Controller](#control)
    * [UI](#ui)
* [Architecture](#arch)
    * [Plugins](#plugins)
    * [Config](#config)
* [Project Requirements](#proj_req)
* [Author](#author)

## Requirements <a id="req"></a>

- Python 3.8.x
- Passlib 1.7.4
- Python-dotenv 1.0.0

[back to top](#top)

## Installation <a id="install"></a>

```
pip install -r requirements.txt
```

[back to top](#top)

## Usage <a id="usage"></a>

> ```TASK_MANAGER``` is a simple CLI app.

![Main menu in CLI](https://github.com/MarFerDom/simpleTaskManager/blob/78cda35e585689796f7d281da5d3a457b9ca5090/ss_main_menu_prompt.png?raw=true)

> ```TASK_MANAGER_GUI``` is a simple GUI app.

![TkInter GUI](https://github.com/MarFerDom/simpleTaskManager/blob/78cda35e585689796f7d281da5d3a457b9ca5090/ss_tk_inter_gui.png?raw=true)

[back to top](#top)

## TODO <a id="todo"></a>

    0. Write a proper README

    1. Brake the app into microservices;

    2. SQL and noSQL database options (local model was part of the bootcamp requirements)

    3. Better UI graphics

[back to top](#top)

## Components <a id="#comp"></a>


### Application Configuration <a id="app_conf"></a>

    File app_config.json contains the app structure.


### Model - Broken down into: <a id="mode"></a>

    1. task_master:

        Implements all task related operations.

    2. user_manager: 

        Implements all user related operations.
    
    3. file_handler:

        Interface for local file handling for all data storage.

### States: <a id="states"></a>

    The states of the app and their transitions are defined in the app_config.json file. Each state is composed of a specific controller that connects to its related UI and some configurable properties. That way some controllers/UIs are used for multiple states with flexibility and simple json editing.

### Controller: <a id="control"></a>

    Implements the controller logic. Composed of the task manager and the task specific controllers: action, insertion, presentation, selection and user operations.

    1. Action deals with states that do not require user interaction;
    2. Insertion deals with states that require the user to enter one or more data;
    3. Presentation deals with states that only present data to the user and wait confirmation;
    4. Selection deals with states that require the user to select from options;
    5. User operations include logging in and creation of new users, hashing and password handling is necessary.

### UI: <a id="ui"></a>

    Implements the UI logic. Always in two flavors, prompt and GUI.

[back to top](#top)

## Architecture <a id="arch"></a>

### Plugins: <a id="plugins"></a>

    Controller and UI modules are loaded as necessary.

### Config: <a id="config"></a>

    Basic app configurations constants.

[back to top](#top)

## Project requirements: <a id="proj_req"></a>

1 - Users and passwords saved as open text in semicolon separated values file.

2 - Tasks composed of 'username', 'title', 'description', 'due date', 'assigned date' and 'completed':
- 'username': Name of registered user resposible for said task;
- 'title': A title for the task;
- 'description': A description of the task;
- 'due date': Final date for delivery of the task in %DD-%MM-&YY format;
- 'assigned date': Date in which the task was assigned in %DD-%MM-&YY format; and
- 'completed': If task is completed, values 'Yes' or 'No'.


3 - User logs in before accessing a menu.

4 - Main menu must have these options:
- Registering a user: Requests one by one the 'username' and 'password'. Does not allow repeated usernames;
- Adding a task: Requests one by one the 'username', 'title', 'description', and 'due date' ;
- View all tasks: View all registered tasks attributes in a easily readable format;
- View my task: Same as view all though only the current user's ones;
- Generate reports: Reports are saved as text files in a readable format according to items 6 and 7 below;
- Display statistics: Print report files content on screen, previously creating if none exists; and
- Exit.

5 - The 'Display statistics' option only shows if logged in as admin.

6 - Statistics calculated and kept in task_overview.txt file include:
- Number of tasks;
- Number of completed tasks;
- Number of incomplete tasks;
- Number of overdue tasks;
- Percentage of incomplete tasks;
- Percentage of overdue tasks.
  
7 - Statistics calculated and kept in user_overview.txt file include:
- Number of tasks;
- Number of users;
- For each user:
    - Number of tasks assigned to that user;
    - Percentage of complete tasks assigned to that user;
    - Percentage of incomplete tasks assigned to that user;
    - Percentage of overdue tasks assigned to that user.

8 - The 'View mine' option must include a numbering system that allows for a user to select a task (-1 to return to main menu). A selected task can be marked as done or (if not completed) edited. Editing allows to change username or due date.

9 - Other specific charcteristics of the prompt and print interface, such as messages, are part of the requirements.

[back to top](#top)

## Author

> [MarFerDom](https://github.com/MarFerDom) wrote the code as a compulsory task for the bootcamp.

[back to top](#top)