import logging
import tkinter as tk
from tkinter import ttk, messagebox
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View(tk.Tk):
    def __init__(self,
                 prompt: str = "LOGIN",
                 success_msg: str = "Login Successful",
                 failure_msg: str = 'Login Failed',
                 operation: str = 'login',
                 *args, **kwargs) -> None:
        
        super().__init__()
        self.title(prompt) 
        self.success_msg = success_msg
        self.failure_msg = failure_msg
        self.operation = operation
        self.geometry("400x400+550+200")
        self.bind("<Return>", self.run)
        self.create_ui()
        self.controller_service = self.noLogin

    def create_ui(self):
        self.frame = ttk.Frame(self, padding=140)
        self.frame.grid()

        # Create the username label
        self.username_label = ttk.Label(self.frame, text="Username")
        self.username_label.pack()

        # Create the username entry
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack()

        # Create the password label
        self.password_label = ttk.Label(self.frame, text="Password")
        self.password_label.pack()

        # Create the password entry
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack()

        if self.operation == 'register':
            # Create the password label
            self.password2_label = ttk.Label(self.frame, text="Confirm password")
            self.password2_label.pack()

            # Create the password entry
            self.password2_entry = ttk.Entry(self.frame, show="*")
            self.password2_entry.pack()

        # Create the login button
        self.login_button = ttk.Button(self.frame, text="Login", command=self.run)
        self.login_button.pack()

        # Create the cancel button
        self.cancel_button = ttk.Button(self.frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack()

        logger.info(f'{self.__class__} UI created')

    def bind_provider(self, call: protocols.ControllerUserService) -> None:
        '''
           Binds the contrller service
        '''

        logger.info(f'{self.__class__} binded to method {call.__name__}')
        self.controller_service = call

    def noLogin(self, *args, **kwargs) -> None:
        logger.info(f'{self.__class__} tried to login but no method binded')
        messagebox.showerror(message="No method binded")

    def run(self, key=None):
        '''
           Checks if the username and password are correct
        '''

        # Get the username and password from the entries
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Check if the username and password are correct
        response = False
        try:
            if self.operation == 'login':
                response = self.controller_service(username, password)
            if self.operation =='register':
                password2 = self.password2_entry.get()
                response = self.controller_service(username, password, password2)
        except protocols.ControllerError as e:
            messagebox.showerror(message=e.args[0])

        if response:
            # Login successful
            logger.info(f'{self.title} successful for user {username}')
            messagebox.showinfo(message=self.success_msg)
            self.destroy() 
        else:
            # Login failed
            logger.info(f'{self.title} failed for user {username}')
            messagebox.showerror(message=self.failure_msg) 


if __name__ == '__main__':
    app = View(operation='register')
    app.bind_provider(lambda *x: True)
    # Start the main loop
    app.mainloop()