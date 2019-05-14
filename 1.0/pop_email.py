import poplib
import smtplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from html.parser import HTMLParser
from email.mime.text import MIMEText
from email.header import Header


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)


# from datetime import datetime
# email = '18129832245@163.com'
# passwd = 'Lin241507'
# pop_server = 'pop3.163.com'


def get_email(email, password, server):
    server = poplib.POP3_SSL(server, '995')
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    # print(server.getwelcome().decode('utf-8'))
    server.user(email)
    server.pass_(password)

    # 邮件数量和占有空间
    # stat()返回 消息的数量 和 消息的总大小
    # print('Messages: %s. Size: %s' % server.stat())

    # list()返回:
    # 服务器的响应
    # 消息列表
    # 消息的大小
    _, mails, _ = server.list()

    # 查看返回列表
    # print(mails)

    # 获取最新的一封邮件，索引号为1开始
    # retr(index)返回：服务器响应 消息所有行 消息字节数
    index = len(mails)
    _, lines, _ = server.retr(index)

    # lines存储邮件原始文本每行并进行解析
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    # 可以根据邮件索引从服务器删除邮件
    # server.dele(index)
    # 关闭邮件
    server.quit()
    resu = print_info(msg)
    return resu


# 编码设置
def guess_charset(my_msg):
    charset = my_msg.get_charset()
    if charset is None:
        content_type = my_msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
        return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
        return value


# indent用于缩进显示，递归打印
def print_info(my_msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = my_msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % (' ' * indent, header, value))
    if my_msg.is_multipart():
        parts = my_msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % (' ' * indent, n))
            print('%s-----------------------------------' % ' ' * indent)
            print_info(part, indent + 1)
            pass
    else:
        content_type = my_msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = my_msg.get_payload(decode=True)
            charset = guess_charset(my_msg)
            if charset:
                content = content.decode(charset)
                # print('%sText: %s' % (' ' * indent, content + '...'))
                html_code = content
                hp = MyHTMLParser()
                hp.feed(html_code)
                hp.close()
                # print(hp.links)
                captcha = hp.links[0].split('=')
                # print(captcha)
                print(captcha[-1])
                return captcha[-1]
        else:
            print('%sAttachment: %s' % (' ' * indent, content_type))


# 发送邮件
def send_email(info=''):
    # 邮件发送人
    sender = {
        'email': '18129832245@163.com',
        'psw': 'Lin241507',
    }

    # 邮件接收者
    receivers = ['leo.lin@longsys.com', '18129832245@163.com']

    # 邮件内容
    text = '此邮件由量产云平台自动化测试系统自动发送，请勿回复！\r\n' + info
    # 邮件附件

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header(sender['email'])  # 发送者
    message['To'] = Header(','.join(receivers))  # 接收者

    # 邮件标题
    subject = '量产云平台自动化测试-' + info
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('smtp.163.com')
        # smtpObj.set_debuglevel(1)
        smtpObj.login(sender['email'], sender['psw'])
        smtpObj.sendmail(sender['email'], receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件")
        print(e)


if __name__ == '__main__':
    send_email()
