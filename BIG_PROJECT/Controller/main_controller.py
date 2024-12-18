from view.main_view import MainView
from model.image_processing import process_all_images_interactive, display_mssv_list

class MainController:
    def __init__(self):
        self.view = MainView(self)

    def run(self):
        self.view.show()

    def process_images(self):
        process_all_images_interactive("Recources/images")

    def get_mssv_list(self):
        return display_mssv_list()
