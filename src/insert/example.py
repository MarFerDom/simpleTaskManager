from src.insert import prompt, GUI, controller
from src import fake

fake.fake_answer = True

if __name__ == '__main__':
    operation_controller = controller.Controller(
        operation=controller._OPERATIONS_[1])
    operation_controller.bind_UI(GUI.View)
    operation_controller.bind_provider(fake.FakeModel())
    operation_controller.run()