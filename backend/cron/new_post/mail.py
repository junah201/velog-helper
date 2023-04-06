import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from models import Post

BACKEND_SERVER_URL = os.environ.get("BACKEND_SERVER_URL", None)
MAIL_SENDER = os.environ.get("MAIL_SENDER", None)
MAIL_PASSWARD = os.environ.get("MAIL_PASSWARD", None)

env = Environment(
    loader=FileSystemLoader('./'),
    autoescape=select_autoescape(['html']),
)


def send_new_post_notice_email(receiver_address: str, post: Post, user_id: str) -> None:
    new_post_notice_template = env.get_template("new_post_notice.html")

    message = MIMEMultipart()
    message['From'] = MAIL_SENDER
    message['To'] = receiver_address
    message['Subject'] = f"{post.title} | 새 글 알림"
    message.attach(MIMEText(new_post_notice_template.render(
        user=post.blog_id,
        title=post.title,
        link=post.link,
        BACKEND_SERVER_URL=BACKEND_SERVER_URL,
        user_id=user_id,
        short_description=post.short_description or "이 글의 요약을 가져오지 못했습니다. (2022.11.21 이전 글 일 가능성이 있습니다.)",
        user_img=post.blog_img,
        released_year=post.created_at.year,
        released_month=post.created_at.month,
        released_day=post.created_at.day
    ), 'html'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(MAIL_SENDER, MAIL_PASSWARD)
    text = message.as_string()
    session.sendmail(MAIL_SENDER, receiver_address, text)
    session.quit()
    print(f'Mail Sent (new_post) "{receiver_address}" "{post.title}"')
