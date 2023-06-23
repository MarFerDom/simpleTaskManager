# Simple Task Manager

Simple Task Manger made during HyperionDev's bootcamp.

## Requirements

- Python 3.8.x
- Passlib 1.7.4
- Python-dotenv 1.0.0


## Installation

```
pip install -r requirements.txt
```

## Usage

    TASK_MANAGER is a simple CLI app.

    TASK_MANAGER_GUI is a simple GUI app.


## TODO

    0. Write a proper README

    1. Brake the app into microservices;

    2. SQL and noSQL database options (local model was part of the bootcamp requirements)

    3. Better UI graphics

## Components


### Application Configuration

    File app_config.json contains the app structure.


### Model - Broken down into:

    1. task_master:

        Implements all task related operations.

    2. user_manager: 

        Implements all user related operations.
    
    3. file_handler:

        Interface for local file handling for all data storage.

### States:

    The states of the app and their transitions are defined in the app_config.json file. Each state is composed of a specific controller that connects to its related UI and some configurable properties. That way some controllers/UIs are used for multiple states with flexibility and simple json editing.

### Controller:

    Implements the controller logic. Composed of the task manager and the task specific controllers: action, insertion, presentation, selection and user operations.

    1. Action deals with states that do not require user interaction;
    2. Insertion deals with states that require the user to enter one or more data;
    3. Presentation deals with states that only present data to the user and wait confirmation;
    4. Selection deals with states that require the user to select from options;
    5. User operations include logging in and creation of new users, hashing and password handling is necessary.

### UI:

    Implements the UI logic. Always in two flavors, prompt and GUI.

## Architecture

### Plugins:

    Controller and UI modules are loaded as necessary.

### Config:

    Basic app configurations constants.