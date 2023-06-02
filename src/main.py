import tkinter
from gui import Application


def main():
    path_video = "resized_video.mp4"
    app = Application(path_video)
    app.run()

    return 0


if __name__ == "__main__":
    main()
