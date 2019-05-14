from declaration import *


def main():
    back_image = games.load_image('img/back.jpg', transparent=False)
    games.screen.background = back_image

    dead = Preview()
    games.screen.add(dead)
    games.screen.mainloop()


if __name__ == "__main__":
    main()
