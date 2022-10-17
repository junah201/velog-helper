from app.common.config import MAIL_SENDER, MAIL_PASSWARD
from app.database.models import Post
from app.common.config import BACKEND_SERVER_URL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_post_notice_email(receiver_address: str, post: Post, user_id: str):
    mail_content = f'''{post.user}님의 새로운 게시물이 업로드되었습니다.
    제목 : {post.title}
    링크 : https://velog.io/@{post.user}/{post.link}

    수신거부 : {BACKEND_SERVER_URL}/subscription/{user_id}?is_subscribe=false
    '''
    message = MIMEMultipart()
    message['From'] = MAIL_SENDER
    message['To'] = receiver_address
    message['Subject'] = f"{post.user}님의 새로운 게시물이 업로드되었습니다."
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(MAIL_SENDER, MAIL_PASSWARD)
    text = message.as_string()
    session.sendmail(MAIL_SENDER, receiver_address, text)
    session.quit()
    print('Mail Sent', receiver_address, post.title)
