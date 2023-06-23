from typing import List, Optional, Tuple
from src import fake
from src.selection import prompt, GUI, controller

class FakeModel(fake.FakeModel):
    def get_all_tasks(self,
                      user: Optional[str] = None) -> Tuple[List[str], List[int]]:
        return ['d', 'e', 'f', 'g'], [3, 7, 8, 12]

if __name__ == '__main__':
    operation_controller = controller.Controller(
        user=fake.FakeUser(),
        model=FakeModel(),
        id=-1,
        source='user',
        options=['a', 'b', 'c']
    )
    operation_controller.bind_UI(GUI.View)
    operation_controller.run()
    print(f'Current id: {operation_controller.id}')
    print(f'Next state: {operation_controller.next}')
