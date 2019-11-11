import ast
from ftplib import FTP
from socket import *

import RealServer.user as u


class cilent(object):
    host = '127.0.0.1'
    port = 2111
    ftphost = '127.0.0.1'
    ftpport = 21

    def __init__(self):
        """
        self.user 用来记录客户端的登陆账户
        self.ftpuser用来记录链接文件服务器的账号密码
        """
        self.user = None
        self.conn = socket(AF_INET, SOCK_STREAM)
        self.addr = ((cilent.host, cilent.port))
        self.conn.connect(self.addr)
        self.ftp = FTP()
        self.ftp.connect(cilent.ftphost, cilent.ftpport)
        self.ftpuser = 'guest'

    def sendregister(self, u_name, u_pass, u_email, u_sex):
        msg = '{"msgtype":0,"name":"%s","pass":"%s","email":"%s","sex":"%s"}' % (u_name, u_pass, u_email, u_sex)
        self.conn.send(msg.encode('utf-8'))
        recvmsg = self.conn.recv(1024).decode('utf8')
        if recvmsg == "注册邮箱已存在":
            print(recvmsg)
        else:
            self.user = u.user(u_name, u_pass, recvmsg[5:], u_sex, u_email)
            print("Congratulations you had succed registed :" + str(self.user))
            # pass

    def sendlog(self, u_m1, u_pass):
        msg = '{"msgtype":1,"EmailOrId":"%s","pass":"%s"}' % (u_m1, u_pass)
        self.conn.send(msg.encode('utf-8'))
        recvmsg = self.conn.recv(1024).decode('utf8')
        print(recvmsg)
        if recvmsg != "用户名或密码错误":
            msg = ast.literal_eval(recvmsg)
            self.user = u.user(msg['name'], msg['pass'], msg['id'], msg['sex'], msg['email'])
            self.ftpuser = 'user'
            #  同时需要进入指定目录
            self.ftp.login(self.ftpuser, self.ftpuser)
            self.ftp.cwd(str(self.user.No))
            print("Congratulations you had succed log in :" + str(self.user))
        else:
            print(recvmsg)

    def sendreset(self, user_id, user_name, user_pass, user_email, user_sex):
        msg = '{"msgtype":2,"id":"%s","name":"%s","pass":"%s","email":"%s","sex":"%s"}' % (
            user_id, user_name, user_pass, user_email, user_sex)
        self.conn.send(msg.encode('utf-8'))
        recvmsg = self.conn.recv(1024).decode('utf8')
        if recvmsg == "修改成功":
            print(recvmsg)
        else:
            print(recvmsg)

    def stylemove(self, imgpath):
        # 执行风格迁移
        # 我想早这个地方使用进程来解决问题
        # 或者设置一下，当用户进行文件处理的时候
        if self.user:
            self.ftpuser = "user"
        msg = '{"msgtype":3}'
        self.conn.send(msg.encode('utf-8'))  # 告诉服务端你将要发送给他的是图片
        m1 = self.conn.recv(1024)
        m1 = m1.decode('utf-8')
        if m1 == 'ready':
            self.upload(imgpath, imgpath)
        else:
            print(m1)
            return
        m1 = self.conn.recv(1024)
        m1 = m1.decode('utf-8')
        if m1 == "finish":
            m1 = self.conn.recv(1024).decode('utf8')
            self.download(m1, "ne梵蒂冈和法规和w" + m1)
        pass

    def upload(self, remote_path, local_path):
        # 从本地上传文件到服务器。
        # 两个参数风别表示远程上传路径，本地文件路径
        # self.ftp.login(self.ftpuser, self.ftpuser)
        fp = open(local_path, "rb")
        buf_size = 1024
        self.ftp.storbinary("STOR {}".format(remote_path), fp, buf_size)
        fp.close()
        self.conn.send(remote_path.encode('utf8'))
        print("Done")

    def download(self, remote_path, local_path):
        # 从本地上传文件到服务器。
        # 两个参数风别表示远程上传路径，本地文件路径
        fp = open(local_path, "wb")
        buf_size = 1024
        self.ftp.retrbinary('RETR {}'.format(remote_path), fp.write, buf_size)
        fp.close()


if __name__ == "__main__":
    # str1 = "你的id为12456"
    # str2 = "你的id为"
    # print(len(str1))
    # str = str1[5:]
    # print(str)
    c1 = cilent()
    while True:
        s1 = input(">>")
        if s1 == "1":
            c1.sendregister("赵思123", "qwertyuiop", "zws@163.com", "W")
        elif s1 == "2":
            c1.sendlog('zws@163.com', 'qwertyuiop')
        elif s1 == "3":
            c1.sendreset(c1.user.No, c1.user.name + "1", c1.user.password, c1.user.email, c1.user.email)
        else:
            c1.stylemove("cat1.jpg")
