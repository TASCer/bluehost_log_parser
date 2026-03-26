import json
import logging
import os
import smtplib
import ssl

from dotenv import load_dotenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import Logger
from pathlib import Path
from ssl import Purpose

load_dotenv()

email_reciever: list[str] = json.loads(os.environ["RECIPIENTS"])
email_sender: str = os.environ["EMAIL_FROM"]
mail_server: str = os.environ["EMAIL_HOST"]
email_user: str = os.environ["EMAIL_USER"]
email_password: str = os.environ["EMAIL_PASSWORD"]


def send_mail(subject: str, text: str, attachment_path: Path | None = None) -> None:
    """
    Function sends email messages.

    :param subject: _description_
    :param text: _description_
    :param attachment_path: _description_, defaults to None
    """
    logger: Logger = logging.getLogger(__name__)

    msg: MIMEMultipart = MIMEMultipart("alternative")
    msg["Subject"] = f"{subject}"
    msg["From"] = email_sender
    msg["To"] = email_reciever[0]

    if attachment_path:
        html_attachments: str = """\
          <html>
            <body>
              <p><b>BH Weblogs Parser Mailer</b></p>
              <br>
              <p>Please find the domain report attached.</p>
              <br>
              <p>Visit below for more information</p>
              <a href="https://tascs.test">TASCS - HOA</a>       
            </body>
          </html>
          """
        with open(attachment_path, "rb") as attachment:
            html: MIMEText = MIMEText(html_attachments, "html")
            part_attachments: MIMEBase = MIMEBase("application", "octet-stream")
            part_attachments.set_payload(attachment.read())
            encoders.encode_base64(part_attachments)
            part_attachments.add_header(
                "Content-Disposition", "attachment", filename=str(attachment_path)
            )
            msg.attach(part_attachments)
            msg.attach(html)
    else:
        html_basic: str = f"""\
            <html>
              <body>
                <p>{text}
                <p><b>BH Weblogs Parser Mailer</b>
                <br>
                   Visit <a href="https://www.tascs.test">TASCS</a> 
                   for more information.
                </p>
              </body>
            </html>
            """
        part_basic: MIMEText = MIMEText(html_basic, "html")
        msg.attach(part_basic)
    # NORMAL PORT 25 METHOD WORKING
    # with smtplib.SMTP(mail_server, 25) as server:
    #     try:
    #         server.sendmail(email_sender, email_reciever, msg.as_string())
    #         logger.info("emil sent")
    #     except smtplib.SMTPException as e:
    #         logger.exception(f"email not sent {str(e)}")

    # PORT 587 w/auth sasl_method = PLAIN phpmailer has it LOG IN

    try:
        with smtplib.SMTP(
            mail_server, 587, local_hostname="tascslt.tascs.local"
        ) as server:
            server.ehlo()
            server.starttls()
            try:
                server.login(email_user, email_password)
            except smtplib.SMTPAuthenticationError as login_err:
                logger.error(f"{login_err}")

            server.sendmail(email_sender, email_reciever, msg.as_string())
            logger.info("email sent")

    except smtplib.SMTPException as err:
        logger.exception(f"{str(err)}")


if __name__ == "__main__":
    send_mail(
        "test sub",
        "test text",
        attachment_path=Path.cwd().parent.parent.parent / "_old_logs" / "11-21-25.log",
    )


# SSL MODULE TESTING [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:997)  1123 on RPI4
# print(ssl.OPENSSL_VERSION)
# context = ssl.create_default_context(purpose=Purpose.SERVER_AUTH)
# context.get_ciphers()
# context.get_ca_certs()
# # context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable SSLv2 and SSLv3
#
#     try:
#         with smtplib.SMTP_SSL(mail_server, 587, local_hostname='tascslt.tascs.local', context=context) as server:
#             server.ehlo()
#             server.starttls()
#             server.login(my_secrets.postfix_user, my_secrets.postfix_password)
#             server.sendmail(my_secrets.mail_from, email_reciever, msg.as_string())
#             logger.info("emil sent")
#
#     except (smtplib.SMTPException) as e:
#         logger.exception(f"{str(e)}")
#
# send_mail(f"Bluehost log processing complete. Public: 2 - SOHO: 2)", "test")

# cert = ssl.get_server_certificate(addr=('tascs.test', 587))#, ssl_version=3, ca_certs=None)
# print(ciphers)
# print(len(ciphers))
# # certs = context.load_default_certs()
# print(len(certs))
# for c in certs:
#     issuer = c.get('issuer')
#     for i in issuer:
#         print(i[0])
# print(issuer[2])
# context.set_ciphers('ALL')        #("TLS_RSA_WITH_AES_128_CBC_SHA256")     # ("TLS_DHE_RSA_WITH_AES_128_GCM_SHA256")
# context.hostname_checks_common_name = False
# context.check_hostname = False
# context.verify_mode = ssl.CERT_NONE
# ser_cert = ssl.get_server_certificate((my_secrets.postfix_mailhost, 587))
# context.load_default_certs()
# ca = context.get_ca_certs()
# c = context.get_ciphers()journ
# ciphers = list({x['name'] for x in c})
# print(ciphers)
# print(ca)
