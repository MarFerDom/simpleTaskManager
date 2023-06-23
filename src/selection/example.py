from typing import List, Optional, Tuple
from src import fake
from src.selection import prompt, GUI, controller

class FakeModel(fake.FakeModel):
    def get_all_tasks(self,
                      user: Optional[str] = None) -> Tuple[List[str], List[int]]:
        mapping = list(range(21))
        return [f'Option {i+1}' for i in mapping], mapping

if __name__ == '__main__':
    operation_controller = controller.Controller(
        user=fake.FakeUser(),
        model=FakeModel(),
        id=-1,
        source='user',
        options=['a', 'b', 'c']
    )
    operation_controller.bind_UI(prompt.View)
    operation_controller.run()
    print(f'Current id: {operation_controller.id}')
    print(f'Next state: {operation_controller.next}')
