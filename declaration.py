from livewires import games, color
import random

games.init(screen_width=900, screen_height=600, fps=50)


class Student(games.Animation):
    sound = games.load_sound('music/jump.wav')
    imgs = []

    def __init__(self, game, x, y):
        for i in range(1, 7):
            Student.imgs.append('img/run' + str(i) + '.png')
        super(Student, self).__init__(images=Student.imgs,
                                      x=x,
                                      y=y,
                                      repeat_interval=8)
        self.game = game
        self.time_till_drop = 0
        self.score = games.Text(value=0,
                                size=100,
                                color=color.dark_red,
                                top=500,
                                right=800)
        games.screen.add(self.score)

    def update(self):
        self.y = 420
        if games.keyboard.is_pressed(games.K_SPACE):
            self.y -= 120
            Student.sound.play()

        self.check_drop()
        self.check()

    def check(self):
        for book in self.overlapping_sprites:
            book.collision()
            book.end_game()

    def check_drop(self):
        if self.time_till_drop > 0:
            self.time_till_drop -= 1
        else:
            obj = random.choice(['book', 'pen'])
            img = games.load_image('img/' + obj + str(random.randint(1, 5)) + '.png')
            new_object = Book(img, student=self)
            games.screen.add(new_object)

            cloud = Cloud()
            games.screen.add(cloud)

            self.time_till_drop = random.randint(70, 130)


class Book(games.Sprite):
    sound_end = games.load_sound('music/end.wav')

    def __init__(self, img, student, x=900, y=400):
        super(Book, self).__init__(image=img,
                                   x=x, y=y,
                                   dx=-5)
        self.student = student

    def update(self):
        if self.left < 0:
            self.destroy()
            self.student.score.value += 1
        self.angle += 2

    def collision(self):
        self.destroy()

    def end_game(self):
        Book.sound_end.play()
        end_message = games.Message(value='YOU LOOOOOSE!!', size=90,
                                    color=color.dark_red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    lifetime=2 * games.screen.fps,
                                    after_death=games.screen.quit)
        games.screen.add(end_message)


class Cloud(games.Sprite):
    img = games.load_image('img/cloud.png')

    def __init__(self, x=1000):
        super(Cloud, self).__init__(image=Cloud.img,
                                    x=x,
                                    y=random.randint(10, 200),
                                    dx=-1)

    def update(self):
        if self.left == -50:
            self.destroy()


class Game:
    games.music.load('music/main.mp3')

    def __init__(self):
        student = Student(game=self, x=200, y=420)
        games.screen.add(student)

    def play(self):
        games.music.play(-1)
        for j in range(4):
            cloud = Cloud(random.randint(100, 900))
            games.screen.add(cloud)


class Preview(games.Animation):
    imgs = []
    sound = games.load_sound('music/preview.wav')

    def __init__(self, x=450, y=300):
        for i in range(1,6):
            Preview.imgs.append('img/text' + str(i) + '.png')
        super(Preview, self).__init__(images=Preview.imgs,
                                      x=x,
                                      y=y,
                                      repeat_interval=30)
        Preview.sound.play()

    def update(self):
        if games.keyboard.is_pressed(games.K_SPACE):
            self.destroy()
            Preview.sound.stop()
            deadline = Game()
            deadline.play()
