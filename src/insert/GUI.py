import logging
import tkinter as tk
from tkinter import ttk, messagebox
from src import protocols

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

class View(tk.Tk):
    def __init__(self,
                 prompt: str = "Enter new value",
                 success_msg: str = "Change Successful",
                 failure_msg: str = 'Change Failed',
                 input_list: list = ['new owner'],
                 line_height: int = 32,
                 *args, **kwargs) -> None:
        super().__init__()
        self.title(prompt) 
        self.success_msg = success_msg
        self.failure_msg = failure_msg
        self.input_list = input_list
        self.num_lines = len(self.input_list)
        if self.num_lines > 10 : raise ValueError('Too many lines')
        _line_height = line_height
        self.geometry(f"510x{_line_height*(self.num_lines+2)}+550+200")
        self.bind("<Return>", lambda x: self.on_confirm())
        self.create_ui()
        self.controller_service: protocols.ControllerInsert = lambda x: False

    def on_confirm(self):
        # So that pressing enter doesn run empty entries.
        if self.button['state'] == 'disabled': return

        new_value = []
        # Get the selected items
        for entry in self.new_entry:
            new_value.append(entry.get())
        
        # Call the controller on the new value.
        try:
            if self.controller_service(new_value):
                messagebox.showinfo(message=self.success_msg)
            else:
                messagebox.showinfo(message=self.failure_msg)
        except protocols.ControllerError as e:
            messagebox.showinfo(message=e.args[0])
        
        # Destroy the window
        self.destroy()

    def create_ui(self):

        def valid():
            '''
               Checks that all entries are filled in.
            '''

            return all([len(e.get()) for e in self.new_entry])

        def validate():
            # Button enabled only when valid.
            if valid():
                # Enable the confirmation button
                self.button.config(state="normal")
            else:
                # Disable the confirmation button
                self.button.config(state="disabled")
            return True

        # Create a frame to hold the widgets
        opts = ('flat', 'raised', 'sunken', 'solid', 'ridge', 'groove')
        self.frame = ttk.Frame(self, relief=opts[5])#, width=1080, height=200)#, padding=20)
        self.frame.pack(fill='both')#grid(column=1)#, padx=15, pady=25)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        for i in range(self.num_lines+4):
            self.frame.rowconfigure(i, weight=1)

        # Create the entries.
        self.label = []
        self.new_entry = []
        i = 1
        for entry in self.input_list:
            # Label
            self.label.append(ttk.Label(self.frame, width=20, text=entry))
            self.label[-1].grid(row=i, column=(i+1)%2, rowspan=1, padx=5)
            # Create the username entry
            self.new_entry.append(ttk.Entry(self.frame, width=50))
            self.new_entry[-1].grid(row=i, column=i%2, rowspan=1, padx=5, pady=5)
            self.new_entry[-1].bind('<KeyRelease>', lambda _: validate())
            i += 2
        
        # Create a button widget to select an item from the listbox
        self.button = tk.Button(self.frame, width=70, state='disabled',
                                text="Confirm", command=self.on_confirm)
        cancel_button = tk.Button(self.frame, width=70, text="Cancel", command=self.destroy)

        # Pack the widgets
        self.button.grid(row=i+1, column=0, columnspan=2, rowspan=1, pady=2)        
        cancel_button.grid(row=i+2, column=0, columnspan=2, rowspan=1)
        logger.info(f'{self.__class__} UI created')

    def bind_provider(self, call: protocols.ControllerInsert) -> None:
        '''
           Binds the function to the method
        '''
        
        logger.info(f'{self.__class__} binded to login method {call.__name__}')
        self.controller_service = call


if __name__ == '__main__':
    input_list = ['a','b','c','d','e','f','g']
    app = View(input_list=input_list)
    # Start the main loop
    app.mainloop()