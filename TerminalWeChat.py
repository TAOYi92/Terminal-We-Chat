#!/usr/bin/env python3
# coding=utf-8
"""
命令行微信聊天
Created on 2017-6-5
Last Modified on 2017-6-28

@author: 德布罗意
"""

import time as t
import _thread
import getpass
import itchat
from itchat.content import *


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def receive(msg):
    """接收微信消息并显示

    :param msg: 接收消息
    :return: 无返回
    """
    type_dict = {'Text': 0, 'Map': 1, 'Card': 2, 'Note': 3, 'Sharing': 4}
    msg_type = ['', '【地图】', '【名片】', '【注示】', '【分享】']
    user_remark = itchat.search_friends(userName=msg['FromUserName'])['RemarkName'] or itchat.search_friends(
        userName=msg['FromUserName'])['NickName'] or 'Unknown'
    if user_remark == 'Unknown':
        print('------- DEBUG output -------\n' + msg + '\n----------------------------')
    if msg['FromUserName'] == itchat.originInstance.storageClass.userName:
        user_remark = '我'
        msg_time = t.asctime(t.localtime(t.time()))
        if msg['ToUserName'] == 'filehelper':
            print('\033[33m{time}  \033[34m{user_from}\033[0m -> '
                  '\033[34m{user_to}\033[0m: \033[1;35m{type}\033[30m{msg}'
                  '\033[0m'.format(time=msg_time, user_from=user_remark, user_to='我',
                                   type=msg_type[type_dict[msg['Type']]], msg=msg['Text']))  # 终端监测
        else:
            user_to = itchat.search_friends(userName=msg['ToUserName'])['RemarkName'] or itchat.search_friends(
                userName=msg['ToUserName'])['NickName']
            print('\033[33m{time}  \033[34m{user_from}\033[0m -> '
                  '\033[35m{user_to}\033[0m: \033[1;35m{type}\033[30m{msg}'
                  '\033[0m'.format(time=msg_time, user_from=user_remark, user_to=user_to,
                                   type=msg_type[type_dict[msg['Type']]], msg=msg['Text']))  # 终端监测
    else:
        msg_time = t.asctime(t.localtime(t.time()))
        print('\033[33m{time}  \033[35m{user_from}\033[0m: \033[1;35m{type}\033[30m{msg}\033[0m'.format(
            time=msg_time, user_from=user_remark, type=msg_type[type_dict[msg['Type']]], msg=msg['Text']))  # 终端监测


def send():
    """发送微信消息或文件

    :return: 无返回
    """
    while True:
        # ipt = input()
        ipt = getpass.getpass('')  # 不显示输入的命令
        # print('\r                                                    \r', end='')
        # 发送消息
        if ipt == 'ss' or ipt == 'sm' or ipt == 'send-msg':
            to_user = input('\033[1;34mTo: \033[0m')
            print('\r                                                    \r', end='')
            msg_text = input('\033[1;32mMsg: \033[0m')
            print('\r                                                    \r', end='')
            if to_user and msg_text:
                friend = itchat.search_friends(remarkName=to_user) or itchat.search_friends(nickName=to_user)
                if friend or to_user == 'filehelper':
                    if to_user == 'filehelper':
                        itchat.send_msg(msg=msg_text, toUserName=to_user)
                    else:
                        itchat.send_msg(msg=msg_text, toUserName=friend[0]['UserName'])
                    print('\033[33m{time}  \033[36mTerminal-Msg-To \033[35m{user}\033[1;34m: \033[30m{msg}'
                          '\033[0m'.format(time=t.asctime(t.localtime(t.time())), user=to_user, msg=msg_text))  # 终端监测
                else:
                    print('\033[31mWarning\033[0m: No such friend.')
        # 发送文件
        elif ipt == 'sf' or ipt == 'send-file':
            to_user = input('\033[1;34mTo: \033[0m')
            print('\r                                                    \r', end='')
            file_name = input('\033[1;32mFile Name: \033[0m')
            print('\r                                                    \r', end='')
            if to_user and file_name:
                friend = itchat.search_friends(remarkName=to_user)
                if friend or to_user == 'filehelper':
                    if to_user == 'filehelper':
                        itchat.send(msg='@fil@{fn}'.format(fn=file_name), toUserName=to_user)
                    else:
                        itchat.send(msg='@fil@{fn}'.format(fn=file_name), toUserName=friend[0]['UserName'])
                    print('\033[33m{time}  \033[36mSend-File-To \033[35m{user}\033[1;34m: 【文件】\033[30m{msg}'
                          '\033[0m'.format(time=t.asctime(t.localtime(t.time())), user=to_user, msg=file_name))  # 终端监测
                else:
                    print('No such friend.')
        # 退出终端版本微信
        elif ipt == 'qq' or ipt == 'quit' or ipt == '退出':
            exit(0)
        # 登出网页版微信
        elif ipt == 'logout':
            itchat.logout()
        # 显示帮助信息--命令提示
        elif ipt == 'hh' or ipt == 'help':
            # 双字符避免误操作
            print('\033[1m****************************************\n'
                  '*     HELP cmd in Terminal-We-Chat     *\n'
                  '****************************************\n'
                  '      Function         Command\033[0m\n'
                  '      help info        hh/help\n'
                  '      send message     ss/send-msg\n'
                  '      send file        sf/send-file\n'
                  '      quit program     qq/quit\n'
                  '      logout wechat    logout\n'
                  '\033[1m****************************************\033[0m')
        else:
            print('\r')


def lc():
    print('Terminal We-Chat Launched Successfully!')

if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=-2, loginCallback=lc)
    _thread.start_new_thread(itchat.run, ())
    _thread.start_new_thread(send(), ())
