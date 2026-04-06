Class Menu:
    def __init__(selection):
        selection.options = ["Add Quiz", "Take Quiz", "Exit"]

    def display(selection):
        print("Menu:")
        for idx, option in enumerate(selection.options, 1):
            print(f"{idx}. {option}")




class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


