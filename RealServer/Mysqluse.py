"""
 数据库操作类
attention
this is the format project file , please design it more carefully!
"""
import pymysql

import RealServer.user as u


class MySql:
    def __init__(self, ip='182.61.61.219', port=3306, user='djh', password='201726010111', database='项目1',
                 charset='utf8'):
        self.mysql = pymysql.connect(
            host=ip,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset
        )

    def queryemail(self, email):
        """
        查询是否存在注册邮箱
        :param user:注册者信息
        :return:
        """
        cursor = self.mysql.cursor()
        sql = "select user_email from user where user_email = '%s';" % (email)
        try:
            cursor.execute(sql)
        except:
            cursor.close()
            return False
        if cursor.rowcount == 1:
            cursor.close()
            return False
        elif cursor.rowcount == 0:
            cursor.close()
            return True

    def queryuser(self, aim: tuple):
        """
        查询数据库,判断id password 是否出错
        :param aim 元组类型（userNo，userpassword): aim是指指定的
        :return:True/False 是否登陆成功
        """
        No, Pass = aim
        cursor = self.mysql.cursor()
        # 可以id或者邮箱登陆
        sql = "select user_name,user_id,user_pass,user_email,user_sex from user where user_pass='%s' and (user_id='%s' or user_email = '%s');" % (
        Pass, No, No)
        try:
            cursor.execute(sql)
        except:
            cursor.close()
            return False
        if cursor.rowcount == 1:
            userinfo = cursor.fetchall()
            cursor.close()
            return userinfo
        cursor.close()
        return False

    def adduser(self, user: u.user):
        sql = "insert into user(user_id,user_name,user_sex,user_email,user_pass)values('%s','%s','%s','%s','%s');" \
              % (user.No, user.name, user.sex, user.email, user.password)
        print(sql)
        flag = False
        cursor = self.mysql.cursor()
        try:
            cursor.execute(sql)
            print("插入成功")
            self.mysql.commit()
            flag = True
        except:
            self.mysql.rollback()
            print("插入失败")
        cursor.close()
        return flag

    def resetuser(self, user: u.user):
        sql = "update user set user_name = '%s',user_email = '%s' ,user_pass = '%s' ,u_sex = '%s'where user_id='%s';" % (
        user.name, user.email, user.password, user.sex, user.No)
        print(sql)
        flag = False
        cursor = self.mysql.cursor()
        try:
            cursor.execute(sql)
            # print("更新成功")
            self.mysql.commit()
            flag = True
        except:
            self.mysql.rollback()
            # print("插入失败")
        cursor.close()
        return flag


if __name__ == "__main__":
    # name=None,password=None,No=None,sex=None,email=None,birthday=None)
    m1 = MySql()
    if m1.queryuser(("djh05", "201726010111")):
        print("yes the customer exsit")
    else:
        print("sorry num or pass error")
    u1 = u.user("张三", "123456", "289653", "男", "1245@example.com", "2001-05-23")
    m1.adduser(u1)
    m1.resetpass(u1, "58698756")
