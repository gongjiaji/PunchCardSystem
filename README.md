# Main features

The staff can register attendence by enter IC number / name or whatever could indicate identity.
- The first punch is 'in'
- From the second punch onward, it's 'out'. If mulitple punches recorded, only the last punch is valid.
The punch records are stored in CSV file, the file name is the staff's IC/name.. etc.

A 'submit' button will be appear every 1st day of the month. The button could send records to the admin's email automatially.

# Dependency

The programme is build on Kivy, a python GUI library. Visit https://kivy.org/#home for more information.


# 主要功能

员工可以输入自己的IC号码进行打卡操作

- 当天的第一次打卡为in
- 当天的第二次及以后为out, 如果打了很多次卡, 保留最后一次打卡为out

打卡信息保存在csv文件里, csv文件名为员工IC号码.

每个月的1号, GUI会显示多一个SUBMIT按钮, 由店长点击讲数据发送给admin进行处理

- 只有店长有权力进行操作
- 店长点击按钮以后, 搜集所有的.csv文件, 自动发送邮件到admin邮箱
- 邮件发送以后, 清楚所有的上月记录, 以便记录新的数据.
- 此时员工打开会建立新的文件
- 关闭程序
