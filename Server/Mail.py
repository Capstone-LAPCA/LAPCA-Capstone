from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
import ssl
import os

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
class Mail:
    def __init__(self, name, email, reportType, *args, **kwargs):
        self.name = name
        self.sender_email = "lapcametric@gmail.com" # TODO: replace with your email address
        self.receiver_email = email # TODO: replace with your recipients
        self.password = ''
        self.msg = MIMEMultipart()
        self.msg["Subject"] = "Your LAPCA Results are here!"
        self.msg["From"] = self.sender_email
        self.msg['To'] =self.receiver_email
        self.reportType = reportType

    def sendMail(self):
        text = """"""

        body_text = MIMEText(text, 'plain')  # 
        self.msg.attach(body_text)  # attaching the text body into msg
        html = """\
        <html>
        <body>
            <p>Hi {},<br>
            <br>
            PFA your {} report <br>
            Thank you. <br>
            </p>
        </body>
        </html>
        """

        body_html = MIMEText(html.format(self.name, self.reportType), 'html')  # parse values into html text
        self.msg.attach(body_html)  # attaching the text body into msg

        ## Image
        # img_name = 'logo_pb.png' # TODO: replace your image filepath/name
        # with open(img_name, 'rb') as fp:
        #     img = MIMEImage(fp.read())
        #     img.add_header('Content-Disposition', 'attachment', filename=img_name)
        #     msg.attach(img)

        ## Attachments in general
        ## Replace filename to your attachments. Tested and works for png, jpeg, txt, pptx, csv
        if(self.reportType == 'LAPCA Score'):
            filename = os.path.abspath('LAPCA_metrics/LAPCA_Score_Pdf/Report.pdf') # TODO: replace your attachment filepath/name
        else:
            filename = os.path.abspath('LAPCA_metrics/Similarity_Score_Pdf/Report.pdf') # TODO: replace your attachment filepath/name

        with open(filename, 'rb') as fp:
            attachment = MIMEApplication(fp.read())
            attachment.add_header('Content-Disposition', 'attachment', filename='Report.pdf')
            self.msg.attach(attachment)

        context = ssl.create_default_context()
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # check connection
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # check connection
            server.login(self.sender_email, self.password)

            # Send email here
            server.sendmail(self.sender_email, self.receiver_email, self.msg.as_string())

        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()
