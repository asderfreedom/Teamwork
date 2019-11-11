import ast
import random
import threading
from socket import *

import RealServer.Mysqluse as ms
import RealServer.user as u


class HandlerConnect(threading.Thread):
    def __init__(self, name, socket):
        """
        连接处理线程，暂定name为连接的addr，socket为连接的socket
        :param name: type = str 为线程名称，暂定为连接ip+port
        :param socket: type = socket 为连接socket 以后此链接的一切相关事务由这个socket进行处理
        self.user user将在未来记录登陆的用户信息
        self.logged 用户是否已经登陆
        ps: 考虑待添加功能：一数据库用户来对数据库进行访问 二 游客登陆的一系列权限
        ps:  等待添加一个用户注销功能
        """
        threading.Thread.__init__(self, name=name)
        self.socket = socket
        self.user = None
        self.logged = False

    def run(self):
        print("{} has soccused connected!")
        while True:
            recv_msg = (self.socket.recv(1024)).decode('utf-8')  # 接收到的信息
            print(recv_msg)
            msg = ast.literal_eval(recv_msg)
            recv_type = msg['msgtype']
            print(msg['msgtype'])
            if not self.logged:
                # 没有登陆的时候，暂时只有注册以及登陆的选项 只要不登陆，线程就会阻塞在这里
                if recv_type == 0:
                    # 如果接收到的信息类型为注册类型，判断是否存在这个邮箱
                    if self.register_manage(msg['email']):
                        # 从信息之中取出注册信息
                        u1 = u.user(msg['name'], msg['pass'],
                                    str(random.randint(10000, 100000 - 1)), msg['sex'], msg['email'])
                        db1 = ms.MySql()
                        flag = db1.adduser(u1)
                        while not flag:
                            # 可能会出现两个user_no相同导致插入失败
                            u1.No = str(random.randint(10000, 100000 - 1))
                            flag = db1.adduser(u1)
                        socket.send(("你的id为%s" % (u1.No)).encode('utf-8'))
                elif recv_type == 1:
                    # 如果接收到的消息类型为登陆类型，则判断是否登陆成功
                    self.login(msg['EmailOrId'], msg['pass'])
                else:
                    print("尚未登陆")
                    self.socket.send("尚未登陆，请登陆后重试".encode('utf8'))
            elif self.logged:
                # 已经登陆了，暂定可以处理修改用户信息以及发送接收图片功能
                if recv_type == 2:
                    # 修改用户信息指令
                    u1 = u.user(msg['name'], msg['pass'], msg['id'], msg['sex'], msg[' email'])
                    self.reset(u1)
                    self.user = u1
                    pass
                elif recv_type == 3:
                    # 接受用户上传并处理图片
                    self.socket.send("ready".encode('utf-8'))
                    self.img_manage()
                    pass

    def img_manage(self):
        f_name = random.randint(100, 1000)
        with open(str(f_name) + ".jpg", 'wb') as f:
            while True:
                fdate = self.socket.recv(1024)
                # if len(fdate) > 3 or fdate != b'EOF':
                if fdate != b'EOF':
                    f.write(fdate)
                    # print("u")
                else:
                    # print(fdate)
                    print("接收完毕")
                    break
        self.socket.send("finish".encode('utf-8'))
        m1 = (socket.recv(1024)).decode('utf-8')
        if m1 == "ready":
            with open(str(f_name) + ".jpg", 'rb') as f:
                while True:
                    fdate = f.read(1024)
                    if fdate:
                        self.socket.send(fdate)
                    else:
                        self.socket.send(b'EOF')
                        print("发送完毕")
                        break

    def reset(self, user):
        db1 = ms.MySql()
        flag = db1.resetuser(user)
        if flag:
            # print("yes")
            self.socket.send("修改成功".encode('utf-8'))
        else:
            # print("no")
            self.socket.send("修改失败".encode('utf-8'))
        pass

    def login(self, token, password):
        # 根据用户传输过来的信息判断是否到了成功
        """
        :param socket: 处理用户的套接字
        :param msg: 发送的用户登陆信息,字典类型（username，userpassword）
        :param token:  用户的登陆标识符，可为email或者id中的任何一个
        :param password:  用户的登陆口令，俗称密码
        :return: 返回是否登陆成功
        """
        # print(msg)
        db1 = ms.MySql()
        flag = db1.queryuser((token, password))
        if not flag:
            self.socket.send("用户名或密码错误".encode('utf-8'))
        else:
            msg1 = '{"name":"%s","id":"%s","pass":"%s","email":"%s","sex":"%s"}' % (
                flag[0][0], flag[0][1], flag[0][2], flag[0][3], flag[0][4])
            # 既然登录成功了，那么就把类中的user对象设置为登陆者的相关信息
            self.user = u.user(flag[0][0], flag[0][2], flag[0][1], flag[0][4], flag[0][3])
            # 都登陆成功了，肯定要把self.logged 设置为真喽
            self.logged = True
            # print(msg1)
            self.socket.send(msg1.encode('utf-8'))

    def register_manage(self, email):
        #    判断是否登陆成功
        db1 = ms.MySql()
        flag = db1.queryemail(email)
        if flag:
            return True
        else:
            self.socket.send("注册邮箱已存在".encode('utf-8'))
            return False
        pass


# 发送信息线程
def tcplinksend(socket, addr):
    """
    多线程并发处理客户端程序
    :param socket: 套接字选择，选择为哪个用户连接服务str
    :param addr: 当前套接字服务用户的地址Tuple
    :return: None
    """
    while True:
        msg = input('输入你要发送的消息：')
        socket.send(msg.encode('utf-8'))


def main():
    tcp_server = socket(AF_INET, SOCK_STREAM)
    # addr = ('175.10.107.58', 2111)
    addr = ('192.168.111.1', 2111)
    tcp_server.bind(addr)
    tcp_server.listen()
    # #我们希望读取的sicket
    # inputs=[tcp_server]
    # #我们希望写出的消息
    # outputs=[]
    print('waiting for connect...')
    while (True):
        #
        # readable,writable,exceptional=select.select(inputs,outputs,inputs)
        c_server, c_addr = tcp_server.accept()
        # 多线程处理多个客户端程序
        tresv = HandlerConnect(name=str(c_addr), socket=c_server)
        tsend = threading.Thread(target=tcplinksend, args=(c_server, c_addr))  # 为当前连接开辟一个新的线程
        tsend.start()
        tresv.start()
    tcp_server.close()  # 每次进行一个连接套接字最后都需要关闭


if __name__ == "__main__":
    main()
