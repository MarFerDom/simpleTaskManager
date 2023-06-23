from src.presentation import prompt, GUI, controller

def fakePresent(*args, **kwargs):
    return '''In the beginning the Universe was created.
This had made many people very angry and has been widely regarded as a bad move.'''
          
if __name__ == '__main__':
    present_controller = controller.Controller(
        prompt="'The Restaurant at the End of the Universe' - Douglas Adams")
    present_controller.bind_UI(GUI.View)
    present_controller.bind_provider(fakePresent)
    present_controller.run()