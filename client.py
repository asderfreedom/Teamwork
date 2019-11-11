import threading
from socket import *

"""
这是客户端程序，这里我们定义一些默认规则：
1：信息传输类型：json 格式：
json{
msgtype:
msg:
}
"""


# class imgSending(threading.Thread):
#     def __init__(self,user_id,addr):


def sendregister(socket, u_name, u_pass, u_email, u_sex):
    msg = '{"msgtype":0,"name":"%s","pass":"%s","email":"%s","sex":"%s"}' % (u_name, u_pass, u_email, u_sex)
    socket.send(msg.encode('utf-8'))


def sendlog(socket, u_m1, u_pass):
    msg = '{"msgtype":1,"EmailOrId":"%s","pass":"%s"}' % (u_m1, u_pass)
    socket.send(msg.encode('utf-8'))


def sendreset(socket, user_id, user_name, user_pass, user_email, user_sex):
    msg = '{"msgtype":2,"id":"%s","name":"%s","pass":"%s","email":"%s","sex":"%s"}' % (
        user_id, user_name, user_pass, user_email, user_sex)
    socket.send(msg.encode('utf-8'))


def sendImg(socket, img):
    msg = '{"msgtype":3}'
    socket.send(msg.encode('utf-8'))  # 告诉服务端你将要发送给他的是图片
    m1 = socket.recv(1024)
    m1 = m1.decode('utf-8')
    print(m1)
    if m1 == "ready":
        with open(img, 'rb') as f:
            while True:
                file_date = f.read(1024)
                if file_date:
                    socket.send(file_date)
                else:
                    print("图片上传成功")
                    socket.send(b"EOF")
                    # socket.send("finish".encode('utf-8'))
                    break
    else:
        return
    # 既然发送完成，接下来就等待服务端发送蹄片进行保存
    m2 = (socket.recv(1024)).decode('utf-8')
    if m2 == "finish":
        socket.send("ready".encode('utf-8'))
        try:
            with open("new" + img, 'wb')as f:
                while True:
                    fdate = socket.recv(1024)
                    # if len(fdate)>3 or fdate != b'EOF':
                    if fdate != b'EOF':
                        f.write(fdate)
                    else:
                        print("图片接收完毕")
                        break
        except:
            print("接受失败")


# def sendmsg(socket):
#     # 当发送exit到服务端时，服务端会发送exit到客户端
#     while True:
#         msgsend=input("请输入你要发送的信息:")
#         if msgsend == 'exit!':
#             break;
#         else:
#             msgsend=json.dumps(msgsend)
#             socket.send(msgsend.encode('utf-8'))

def resvmsg(socket):
    while True:
        msgresv = socket.recv(1024 * 32)
        msgresv = msgresv.decode('utf-8')
        if msgresv == 'exit!':
            socket.close()
            print('连接已经中断!')
            break;
        print(msgresv)


def connect():
    tcp_connector = socket(AF_INET, SOCK_STREAM)  # 无论调用哪个发送信息代码，其socket变量都是这个
    addr = ('127.0.0.1', 2111)
    # addr = ('182.61.61.219', 2111)
    tcp_connector.connect(addr)
    threads = []
    # 信息发送线程
    # tsend=threading.Thread(target=sendmsg , args=(tcp_connector ,))#args接受一个元组参数，所以加一个括号
    # threads.append(tsend)
    # 信息接收线程
    # sendregister(tcp_connector,'zhangsan','wtest123','test@qq.com','m')
    sendlog(tcp_connector, 'dfhdjfsh@163.com', 'qwertyuiop')
    # sendreset(tcp_connector, "33405", 'zhangsan', 'wtest123', 'test@qq.com', 'm')
    # sendImg(tcp_connector,"cat1.jpg")
    tresv = threading.Thread(target=resvmsg, args=(tcp_connector,))
    threads.append(tresv)
    for i in range(len(threads)):
        threads[i].start()
    threads[0].join()
    tcp_connector.close()


def main():
    connect()


if __name__ == "__main__":
    main()
