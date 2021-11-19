"""powered by Yeloki & FNC"""
from app import App
from drawable import *
from layout import Layout


class TowerDefence(App):
    def __init__(self):
        super(TowerDefence, self).__init__()
        self.count = 0
        self.layout = Layout()
        button = Button(10, 10, 100, 50)
        button.set_text("ADD 1")
        button.connect(self.handler1)
        label = TextLabel(200, 200, 200, 100)
        label.set_style(text_color=Color("red"))
        self.layout.add_element(button)
        self.layout.add_element(label)

    def handler1(self):
        self.set_caption(str(self.count))
        self.count += 1

    def update(self):
        super(TowerDefence, self).update()
        self.layout.update()

    def draw(self):
        self.layout.draw(self.screen)


if __name__ == '__main__':
    td = TowerDefence()
    td.run()
