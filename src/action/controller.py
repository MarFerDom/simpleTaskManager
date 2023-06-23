from src import protocols

ESCAPE_ESTATE = 'main menu'

class Controller:
    def __init__(self,
                 user: protocols.user_protocol,
                 model: protocols.model_protocol,
                 id: int = -1,
                 next: str = 'Null',
                 option: str = 'generate',
                 *args, **kwargs):
        
        self.user = user
        self.model = model
        self.id = id
        self.next = next
        self.option = option
        
        super().__init__()

    def bind_UI(*args, **kwargs):
        pass
    
    def run(self):
        '''
            Execute simple command.

            Uses no UI just, runs a simple command.
            Implements both generate report and mark as done.
        '''

        # If option is none, do nothing
        if self.option == 'none':
            return
        # If generating report, write report to file.
        if self.option == 'generate':
            self.model.write_report(userlist=list(self.user.users))
        # If marking as done, use task id.
        else:
            self.model.mark_as_completed(task_id=self.id)

        # Return to main menu
        #self.next = ESCAPE_ESTATE
        # Reset id at the end for next state.
        self.id = -1