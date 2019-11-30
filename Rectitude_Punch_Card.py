"""
users.txt文件存着员工的名字
如果是3个人的话正好
如果是4个人的话需要增加 build()里的btn_X, 以及 def confirmX, 并把self=name设置为相应的人
"""

import sendEmail as se
import os

os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.config import Config

Config.set("graphics", "resizable", False)
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "450")

from kivy.core.window import Window

Window.clearcolor = (40 / 255, 44 / 255, 52 / 255, 1)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import kivy.uix.popup as pop
import kivy

kivy.require("1.11.0")
import time
import csv


class Rectitude_Punch_Card(App):

    name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label_time = Label(
            text=self.display_time(),
            color=(252 / 255, 138 / 255, 22 / 255, 1),
            font_size=30,
            halign="auto",
            valign="center",
            size_hint=(0.8, 1),
        )
        with open("users.txt", "r") as file:
            self.users = file.readline().split(",")

    def build(self):
        box = BoxLayout(orientation="vertical", spacing=20)
        userButtons = BoxLayout(orientation="horizontal", spacing=5)
        labelBox = BoxLayout(orientation="horizontal", spacing=5)

        # 为每个人增加一个按钮.
        btn_0 = Button(
            text=self.users[0],
            color=(30 / 255, 228 / 255, 147 / 255, 1),
            background_color=(71 / 255, 69 / 255, 69 / 255, 1),
            font_size=50,
            on_press=self.confirm0,
        )

        btn_1 = Button(
            text=self.users[1],
            color=(30 / 255, 228 / 255, 147 / 255, 1),
            background_color=(71 / 255, 69 / 255, 69 / 255, 1),
            font_size=50,
            on_press=self.confirm1,
        )

        btn_2 = Button(
            text=self.users[2],
            color=(30 / 255, 228 / 255, 147 / 255, 1),
            background_color=(71 / 255, 69 / 255, 69 / 255, 1),
            font_size=50,
            on_press=self.confirm2,
        )

        button_submit = Button(
            text="SUBMIT",
            font_size=30,
            color=(222 / 255, 28 / 255, 75 / 255, 1),
            background_color=(0, 0, 0, 1),
            on_press=self.send_out_by_Email,
            size_hint=(0.2, 0.4),
        )

        # if self.get_day() == "1" or self.get_day() == "2":
        #     box.add_widget(button_submit)
        labelBox.add_widget(self.label_time)
        labelBox.add_widget(button_submit)
        userButtons.add_widget(btn_0)
        userButtons.add_widget(btn_1)
        userButtons.add_widget(btn_2)
        box.add_widget(userButtons)
        box.add_widget(labelBox)

        return box

    def get_nric(self, args):
        nric = self.name
        return str(nric).upper()

    @staticmethod
    def get_time():
        localtime = time.localtime(time.time())
        hour = str(localtime[3])
        minute = str(localtime[4])
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute

        return str(hour + ":" + minute)

    @staticmethod
    def get_day():
        localtime = time.localtime(time.time())
        return str(localtime[2])

    def display_time(self):
        return time.asctime(time.localtime(time.time()))

    def confirm0(self, args):
        self.name = self.users[0]
        print(self.get_time() + "       " + self.get_nric(1))
        self.submit()

    def confirm1(self, args):
        self.name = self.users[1]
        print(self.get_time() + "       " + self.get_nric(1))
        self.submit()

    def confirm2(self, args):
        self.name = self.users[2]
        print(self.get_time() + "       " + self.get_nric(1))
        self.submit()

    def get_csv(self):
        path = self.get_nric(1) + ".csv"
        self.data = []

        try:
            with open(path) as f:
                reader = csv.reader(f)
                for row in reader:
                    # data ==> [['18', '08:00', '19:00'], ['19', '09:00', '20:00']]
                    self.data.append(row)

        except FileNotFoundError:
            print("not found")
            with open(path, "a") as f:
                print("create new")
                header = ["Day", "In", "Out"]
                self.data.append(header)
                f.close()

    def write_csv(self):
        """
        1. 文件格式为
            day, in, out
            20, 07:00, 19:00
            21, 06:00, 18:00
        2. 先读取文件, 如果没有这个文件, 创建这个空文件
        3. 读取文件后, 把数据复制到data里面, data是一个二维数组, 每一个元素是day数组
        4. day数组包含3个元素, 日子, in 和 out
        5. 在写入数据的时候先获取日子, 然后遍历查找这个日子, 如果有的话, 添加out
        6. 遍历结束, 如果没有这个日子, 说明是in. 增加一行
        """

        today = self.get_day()
        path = self.get_nric(1) + ".csv"
        day = []  # day ==> ['10','08:00','18:00']

        index = 0
        # out
        for row in self.data:
            index += 1
            if row[0] == today:
                row.append(self.get_time())

        if index == len(self.data) and self.data[index - 1][0] != today:
            day.append(self.get_day())
            day.append(self.get_time())
            self.data.append(day)

        for row in self.data:
            if len(row) >= 3:
                row[2], row[-1] = row[-1], row[2]

        print(self.data)

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

    def send_out_by_Email(self, args):
        se.sendEmail().send()

    def submit(self):
        """
        1. 获取NRIC
        2. 打开文件, 获取之前的数据, 或者新建文件
        3. 写数据
        """
        self.get_csv()
        self.write_csv()
        self.message(self.name)

    def message(self, name):
        box = BoxLayout(orientation="horizontal", spacing=40)
        finish = Button(text="Next Staff")
        close = Button(text="Close Software")
        box.add_widget(finish)
        box.add_widget(close)

        popup = pop.Popup(
            title="ok",
            content=box,
            size_hint=(None, None),
            size=(600, 600),
            auto_dismiss=False,
        )
        finish.bind(on_press=popup.dismiss)
        close.bind(on_press=self.close_programme)

        popup.open()

    def message_submit(self):
        box = BoxLayout(orientation="vertical", spacing=40)
        label = Label(text="Records submitted !", size_hint=(1, 0.7))
        button = Button(text="Close Software!", size_hint=(1, 0.2))
        blank = Label(size_hint=(1, 0.1))
        box.add_widget(label)
        box.add_widget(button)
        box.add_widget(blank)
        popup = pop.Popup(
            title="ok",
            content=box,
            size_hint=(None, None),
            size=(600, 600),
            auto_dismiss=False,
        )
        button.bind(on_press=self.close_programme)
        popup.open()

    def close_programme(self, args):
        App.stop(self, 1)


if __name__ == "__main__":
    app = Rectitude_Punch_Card()
    app.run()
