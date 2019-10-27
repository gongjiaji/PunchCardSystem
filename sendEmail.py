import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import getFileNames as gfn
import Rectitude_Punch_Card as rpc

class sendEmail():
    def send(self):
        # 第三方 SMTP 服务
        mail_host="smtp.gmail.com"  
        mail_user="enter your email address here"    
        mail_pass="enter your password here"    

        receivers = ["enter admin's address here"]

        subject = 'Subject'
        from_name = 'From'
        to_name = 'To'
        message_content = '''
        '''


        files= gfn.getFileNames().operate_csvs(1)

        # file1 = str(files)

        message = MIMEMultipart()
        message['From'] = Header(from_name, 'utf-8')   
        message['To'] =  Header(to_name, 'utf-8')      
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(message_content, 'plain', 'utf-8'))


        # iterate the files
        # 构造附件
        for file in files:
            att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            filename="filename="+file
            att["Content-Disposition"] = 'attachment;'+filename
            message.attach(att)

        try:
            smtpObj = smtplib.SMTP(mail_host,25)
            smtpObj.starttls() 
            smtpObj.login(mail_user,mail_pass)
            smtpObj.sendmail(mail_user, receivers, message.as_string())
            print ("邮件发送成功")
            gfn.getFileNames().operate_csvs(2)
            rpc.Rectitude_Punch_Card().close_programme()
        except smtplib.SMTPException as e:
            print ("Error: 无法发送邮件.    "+e)


