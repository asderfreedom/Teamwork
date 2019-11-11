import smtplib  # 发送邮件模块
from email.header import Header  # 定义邮件标题
from email.mime.text import MIMEText  # 定义邮件内容


def sendEmail(receiver, msg):
    smtpserver = 'smtp.163.com'  # wang yi de you jian fu wu
    user = 'asderfree@163.com'  # 已经开通邮件服务的用户名与密码
    password = '200525djhDJH'
    sender = 'asderfree@163.com'
    # 发送邮件主题和内容
    subject = '咸鱼迁移服务'  # 显示在用户手机上的邮件信息
    content = '<html><h1 style="color:red">咸鱼迁移密码修改:</h1>' \
              '<h2 style="color:blue">%s<h2></html>' % (msg)  # 邮件形式
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'asderfree@163.com'
    msg['To'] = receiver
    # SSL协议端口号要使用465
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    # HELO 向服务器标识用户身份
    smtp.helo(smtpserver)
    # 服务器返回结果确认
    smtp.ehlo(smtpserver)
    # 登录邮箱服务器用户名和密码
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


sendEmail('2467305390@qq.com', '454874')

#
# # 发送邮箱服务器  这个可以自选，我用的时网易
# smtpserver = 'smtp.163.com'
#
# # 发送邮箱用户名密码  这个应该是用来登陆网易邮箱的
# user = 'asderfree@163.com'
# password = '200525djhDJH'
#
# # 发送和接收邮箱
# sender = 'asderfree@163.com'
# receive = '3302860184@qq.com'
#
# # 发送邮件主题和内容
# subject = 'Web Selenium 自动化测试报告'  #显示在用户手机上的邮件信息
# content = '<html><h1 style="color:red">自动化测试报告!</h1></html>' #邮件形式
#
# # HTML邮件正文
# msg = MIMEText(content, 'html', 'utf-8')
# msg['Subject'] = Header(subject, 'utf-8')
# msg['From'] = 'asderfree@163.com'
# msg['To'] = '3302860184@qq.com'
#
# # SSL协议端口号要使用465
# smtp = smtplib.SMTP_SSL(smtpserver, 465)
#
# # HELO 向服务器标识用户身份
# smtp.helo(smtpserver)
# # 服务器返回结果确认
# smtp.ehlo(smtpserver)
# # 登录邮箱服务器用户名和密码
# smtp.login(user, password)
#
# print("开始发送邮件...")
# smtp.sendmail(sender, receive, msg.as_string())
# smtp.quit()
# print("邮件发送完成！")
