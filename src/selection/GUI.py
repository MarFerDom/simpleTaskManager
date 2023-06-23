import logging
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View(tk.Tk):
    def __init__(self, prompt='Prompt',
                 options: List[str] = ['exit'],
                 *args, **kwargs) -> None:
        super().__init__()
        self.title('Select an option')
        self.prompt = prompt
        self.options = options
        self.create_ui()
        self.controller_service = lambda x: None
        self.bind("<Return>", lambda *_:self.on_confirm())

    def on_confirm(self):
        if not self.listbox.curselection(): return
        # Get the selected items
        # selected_items = self.listbox.get(self.listbox.curselection())
        # Call the controller on the selected action.
        self.controller_service(int(self.listbox.curselection()[0]))
        
        # Destroy the window
        self.destroy()

    def create_ui(self):
        def on_select(event):
            # Check if any items are selected
            if self.listbox.curselection():
                # Enable the confirmation button
                self.button.config(state="normal")
            else:
                # Disable the confirmation button
                self.button.config(state="disabled")

        width = 280
        height = 250
        f_width = 270
        f_height = 240
        box_width = 40
        box_height = 12
        self.geometry(f"{width}x{height}+550+200")
        #self.columnconfigure(0,weight=1)
        #self.columnconfigure(1,weight=1)
        #self.columnconfigure(2,weight=1)

        # Create a frame to hold the widgets
        opts = ('flat', 'raised', 'sunken', 'solid', 'ridge', 'groove')
        self.frame = ttk.Frame(self, relief=opts[5], width=f_width,
                               height=f_height, padding=(width -f_width)//2)
        #self.frame.grid(column=0)#, sticky='NS')#, padx=5, pady=5)
        self.frame.pack(fill='both')
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.grid_propagate(False)

        self.frame_title = ttk.Frame(self.frame, width=f_width)
        self.frame_title.grid(row=0)
        self.frame_up = ttk.Frame(self.frame, width=f_width)
        self.frame_up.grid(row=1)
        self.frame_down = ttk.Frame(self.frame, width=f_width)
        self.frame_down.grid(row=2)

        self.titlebox = tk.Listbox(self.frame_title,
                                  width=box_width,
                                  height=box_height//2,
                                  justify='left')
        self.titlebox.insert("end", *self.prompt.splitlines())

        # Create a scrollbar for the listbox.
        scrollbar = tk.Scrollbar(self.frame_up)      
        scrollbar.pack(side='right', fill='both')

        # Create a listbox widget to display the items.
        self.listbox = tk.Listbox(self.frame_up,
                                  width=box_width,
                                  height=box_height//2,
                                  yscrollcommand=scrollbar.set,
                                  justify='left')
        
        scrollbar.config(command = self.listbox.yview)
        
        # Insert options.
        self.listbox.insert("end", *self.options)
        # If item selected.
        self.listbox.bind("<<ListboxSelect>>", on_select)

        # Create a button widget to select an item from the listbox.
        self.button = ttk.Button(self.frame_down, state='disabled',
                                text="Select Item", command=self.on_confirm)
        
        # Create the cancel button
        cancel_button = ttk.Button(self.frame_down,
                                       text="Cancel",
                                       command=lambda:[
                                           self.controller_service(-1),
                                           self.destroy()])
        
        # Pack the widgets
        self.titlebox.pack(fill = 'both')
        self.listbox.pack(fill = 'both')
        self.button.pack(side='left', fill='y')
        cancel_button.pack(side='right')
        logger.info(f'{self.__class__} UI created')

    def bind_provider(self, call: protocols.ControllerSelect) -> None:
        '''
           Binds the function to the method
        '''

        logger.info(f'{self.__class__} binded to\
                     selection method {call.__name__}')
        self.controller_service = call

    def noActions(self, *args, **kwargs) -> None:
        logger.info(f'{self.__class__} tried to run but no method binded')
        messagebox.showerror(message="No method binded")


if __name__ == '__main__':

    # A multi lined prompt for title
    prompt = '''There once was a man called Jeff.
    He was a very good man.
    He was a very bad man.
    He was a very ugly man.
    He was a very fat man.
    He was a very stupid man.
    He was a very lazy man.
    He was a very rich man.'''

    # A set of options to select from.
    options = [f'Option {i}' for i in range(1,20)]
    app = View(options=options.copy(), prompt=prompt)

    # Included an exit option to represent normal app exiting option -1.
    options.append('Cancel')
    # Bind a messagebox as a provider for the selection method.
    app.bind_provider(
        lambda x: messagebox.showinfo(message=f'Selected option: {options[x]}') #type: ignore
        )
    # Start the main loop
    app.mainloop()