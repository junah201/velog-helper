from app.common.config import MAIL_SENDER, MAIL_PASSWARD
from app.database.models import Post
from app.common.config import BACKEND_SERVER_URL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_mail_content_by_post(post: Post, user_id: str):
    env = Environment(
        loader=FileSystemLoader('app/templates/'),
        autoescape=select_autoescape(['html']),
    )
    template = env.get_template("new_post_notice.html")
    return template.render(user=post.user, title=post.title, link=post.link, BACKEND_SERVER_URL=BACKEND_SERVER_URL, user_id=user_id)


def send_post_notice_email(receiver_address: str, post: Post, user_id: str):
    mail_content = get_mail_content_by_post(post, user_id)
    message = MIMEMultipart()
    message['From'] = MAIL_SENDER
    message['To'] = receiver_address
    message['Subject'] = f"{post.user}님의 새로운 게시물이 업로드되었습니다."
    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(MAIL_SENDER, MAIL_PASSWARD)
    text = message.as_string()
    session.sendmail(MAIL_SENDER, receiver_address, text)
    session.quit()
    print('Mail Sent', receiver_address, post.title)
