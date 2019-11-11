import logging
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class tcpserver(threading.Thread):
    """
    这是文件传输线程，只处理文件传输相关任务
    在服务器端其具体的相关功能则是只有等待连接以及处理文件请求了
    """
    HOST = '0.0.0.0'
    port = 21

    def __init__(self):
        threading.Thread.__init__(self)
        # 实例化初始用户，注意，这里我并没有考虑动态的像之前那个主线程处理十五服务器一样给他加上类似于
        # 注册一个用户就去给他添加上一个可以登陆处理的用户，主要考虑到ftp服务器的用户必须关闭服务器重启才有效
        # 这么做可能会造成一部分安全问题，但是我觉得可以接受
        self.users = DummyAuthorizer()
        self.users.add_user('guest', 'guest', 'E:/Desktop/spyder/Projects/Server/data/share', perm="lr")
        self.users.add_user('user', 'user', 'E:/Desktop/spyder/Projects/Server/data/', perm="elrwafm")
        # 用户类型分为两种，一种就是游客模式，一种则是普通用户模式，具体登陆后则可以切换到对应的文件夹目录下
        self.handler = FTPHandler
        self.handler.authorizer = self.users
        self.handler.passive_ports = range(2500, 3000)
        # 文件传输日志信息
        self.logging_name = 'tcp.log'
        # 绑定端口以及ip
        self.server = FTPServer((tcpserver.HOST, tcpserver.port), self.handler)
        # 最多同时50个连接
        self.server.max_cons = 50

        pass

    def run(self):
        # 写入日志信息
        print("ready")
        logging.basicConfig(filename=self.logging_name, level=logging.INFO)
        self.server.serve_forever()


if __name__ == "__main__":
    flag = True
    while True:
        if flag:
            tcpserver().start()
            flag = False
