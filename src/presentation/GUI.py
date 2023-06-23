import logging
import tkinter as tk
from tkinter import ttk, messagebox
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View(tk.Tk):
    def __init__(self, prompt: str = "Title",
                 *args, **kwargs) -> None:
        super().__init__()
        self.title(prompt) 
        self.geometry("600x500+550+200")
        self.bind("<Return>", lambda x: self.destroy()) #type: ignore
        self.create_ui()

    def create_ui(self):
        # Create a frame to hold the widgets

        opts = ('flat', 'raised', 'sunken', 'solid', 'ridge', 'groove')
        self.frame = ttk.Frame(self, relief=opts[5], width=550, height=450)#, padding=20)
        self.frame.grid(column=1, padx=15, pady=5)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.grid_propagate(False)

        # Create a listbox widget to display the items
        self.listbox = tk.Listbox(self.frame, width=90, height=25)
        # Create the cancel button
        self.cancel_button = ttk.Button(self.frame, text="Return", command=self.destroy)
        # Pack the widgets
        self.listbox.grid(row=1)      
        self.cancel_button.grid(row=2, rowspan=2)

        logger.info(f'{self.__class__} UI created')

    def bind_provider(self, call: protocols.ControllerPresent) -> None:
        '''
           Binds the present function and runs it.
        '''

        logger.info(f'{self.__class__} binded to method {call.__name__}')
        self.controller_present = call
        # Present content
        for line in self.controller_present().split('\n'):
            self.listbox.insert("end", line)


if __name__ == '__main__':
    app = View('The big presentaion')
    app.bind_provider(lambda:'''This is a presentation.
It has many lines.

I wonder if it\'ll be okay.''')
    # Start the main loop
    app.mainloop()