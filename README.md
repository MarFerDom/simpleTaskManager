# simpleTaskManager
Simple task manger made during HyperionDev's bootcamp

# TODO

0. Write a proper README
1. App structure defined in config file;
2. Microservices;
3. SQL and noSQL database options
4. CD
5. Better UI graphics

# Components

1. Controller
2. UI
3. Model

# Controller
- options menu

# UI
- login
    |- view
    |- prompt
- selection
    |- view
    |- prompt

# Model

# Others
- file handler
- plugin
- config


### Controller
# Create controller.
    ```
    # Create controller.
    controller = Controller()

    # Bind login provider and UI.
    controller.set_login(LOGIN_METHOD)
    controller.bind_login(LOGIN_UI)

    # Create MAIN_MENU_CONTROLLER
    # ...

    # Bind selection menu controller
    controller.bind_menu(MAIN_MENU_CONTROLLER)

    # Run controller.
    controller.run()
    ```