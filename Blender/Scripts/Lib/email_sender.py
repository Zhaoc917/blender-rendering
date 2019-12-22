#! /usr/bin/env python
#coding=utf-8

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from smtplib import SMTP_SSL
import os
import sys
import datetime
import socket
import json
import getpass
sys.path.append("..")
sys.path.append("../../")
from Lib.ConfigClass import Config


class Email:
    def __init__(self):
        self.host_server = 'smtp.qq.com'
        self.sender = '840092037@qq.com'
        self.password = 'bnktgmlqoefubbbe'
        self.receiver = 'zhaoc@ios.ac.cn'
        self.mail_content = None
        self.image_path = None
        self.video_path = None
        self.mail_title = "Render Task Done!"
        self.video_name = "video.mp4"
        self.config = Config()

    def send_email(self):
        with open(self.config.config_save_path, 'r') as load_f:
            load_dict = json.load(load_f)
        # update
        self.config.__dict__ = load_dict

        self.image_path = self.config.output_path
        self.video_path = self.config.output_path + "/../video/result.mp4"
        # ssl
        smtp = SMTP_SSL(self.host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender, self.password)

        message = MIMEMultipart('mixed')
        # text
        # message.attach(MIMEText(self.mail_content, "plain", "utf-8"))
        message.attach(MIMEText(json.dumps(self.config.__dict__,  sort_keys=True, indent=4).replace(' ', '&nbsp;').replace('\n', '<br>'), "HTML", "utf-8"))
        message["From"] = self.sender
        message["To"] = self.receiver
        message["Subject"] = Header(self.mail_title, 'utf-8')
        # video attachment
        att1 = MIMEText(open(self.video_path, "rb").read(), "base64", "utf-8")
        att1["Content-Type"] = "video/mp4"
        att1["Content-Disposition"] = "attachment;filename=" + self.video_name
        message.attach(att1)

        # image
        att2 = MIMEImage(open(self.image_path, 'rb').read())
        att2.add_header('Content-ID', '<image1>')
        message.attach(att2)

        smtp.sendmail(self.sender, self.receiver, message.as_string())
        smtp.quit()