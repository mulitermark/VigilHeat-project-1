import tkinter
from gui import Application


def main():
    queue_sector = [400, 100, 800, 700]
    app = Application(path_video, queue_sector)
    app.run()

    return 0


if __name__ == "__main__":
    main()
