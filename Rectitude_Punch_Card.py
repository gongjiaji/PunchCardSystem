from kivy.app import App
import kivy
import time
import csv

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

kivy.require('1.11.0')


class Rectitude_Punch_Card(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.x = TextInput(font_size=50, multiline=False, halign="center")
        self.label_time = Label(text=self.display_time(
        ), font_size=100, halign='auto', valign='center')

    def build(self):
        box = BoxLayout(orientation='vertical', spacing=50)
        label = Label(text='Enter NRIC No. below:', font_size=40)
        button = Button(text='Register Attendance', background_color=(
            0, 0, 1, 1), font_size=40, on_press=self.get_nric)
        button_test = Button(text='display test message', on_press=self.test)

        box.add_widget(self.label_time)
        box.add_widget(label)
        box.add_widget(self.x)
        box.add_widget(button)
        box.add_widget(button_test)

        return box

    def get_nric(self, args):
        nric = self.x.text
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

    def test(self, args):
        print(self.get_time()+"       "+self.get_nric(1))
        self.submit()

    def get_csv(self):
        today = self.get_day()
        path = self.get_nric(1) + ".csv"
        self.data = []

        try:
            with open(path) as f:
                reader = csv.reader(f)
                for row in reader:
                    # data ==> [['18', '08:00', '19:00'], ['19', '09:00', '20:00']]
                    self.data.append(row)

        except FileNotFoundError as identifier:
            with open(path, 'a') as f:
                pass

    def write_csv(self):
        '''
        1. 文件格式为
            day, in, out
            20, 07:00, 19:00
            21, 06:00, 18:00

        2. 先读取文件, 如果没有这个文件, 创建这个空文件

        3. 读取文件后, 把数据复制到data里面, data是一个二维数组, 每一个元素是day数组

        4. day数组包含3个元素, 日子, in 和 out

        5. 在写入数据的时候先获取日子, 然后遍历查找这个日子, 如果有的话, 添加out

        6. 如果没有这个日子, 说明是in.
        '''

        today = self.get_day()
        path = self.get_nric(1) + ".csv"
        day = []  # day ==> ['10','08:00','18:00']

        # out
        for row in self.data:
            if(row[0] == today):
                row.append(self.get_time())

        # TODO in

        # TODO csv末尾有两行空白文件, 导致 上面的循环 out of index

        with open(path, 'w', newline="") as f:
            writer = csv.writer(f)
            self.data.append(day)
            writer.writerows(self.data)

    def submit(self):
        '''
        1. 获取NRIC
        2. 打开文件, 获取之前的数据, 或者新建文件
        3. 写数据
        '''
        self.get_csv()
        self.write_csv()


if __name__ == '__main__':
    app = Rectitude_Punch_Card()
    app.run()
