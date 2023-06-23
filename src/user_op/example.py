from src import fake
from src.user_op import prompt, GUI, controller

fake.fake_answer = True
    
if __name__ == '__main__':
    ops = ['login', 'register']
    operation_controller = controller.Controller(operation=ops[1])
    operation_controller.bind_UI(GUI.View)
    operation_controller.bind_provider(fake.FakeUser())
    operation_controller.run()