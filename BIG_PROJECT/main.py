# main.py
from Controller.main_controller import MainController
from model.database import init_db


def main():
    # Khởi tạo cơ sở dữ liệu
    init_db()

    # Khởi chạy ứng dụng
    controller = MainController()
    controller.run()


if __name__ == "__main__":
    main()
