import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
This test log in, send letter and check the letter was delivered
Using smtplib for sending lettters and imaplib for getting information about our mail
"""

# Enter data
sender = "Yuriy.Komrakov@ukr.net"
recipient = "Yuriy.Komrakov@ukr.net"
password = "0937536859yk"
subject = 'Test subject'

# Create our letter using MIMEMultipart
msg = MIMEMultipart()
msg['From']    = sender
msg['To']      = recipient
msg['Subject'] = subject
body = "Test text"
msg.attach(MIMEText(body, 'plain'))

# Make connection to have number of inbox letters before sending new letter
mail_connection = imaplib.IMAP4_SSL("imap.ukr.net")
mail_connection.login(sender, password)
mail_connection.list()
total_letters = str(mail_connection.select("inbox"))
total_letters_before_sending = int(total_letters.split('\'')[3])
mail_connection.__exit__()

# Send new letter
smtp_server = smtplib.SMTP_SSL("smtp.ukr.net", 465)
smtp_server.login(sender, password)
smtp_server.send_message(msg)
smtp_server.quit()

# Get number of inbox letter after sending the letter
mail_connection = imaplib.IMAP4_SSL("imap.ukr.net")
mail_connection.login(sender, password)
mail_connection.list()
total_letters = str(mail_connection.select("inbox"))
total_letters_after_sending = int(total_letters.split('\'')[3])

# Compare inbox letters before and after sending
assert (int(total_letters_before_sending) == (total_letters_after_sending-1))


# Get data from the last letter
typ, data = mail_connection.search(None, "ALL")
id_list = data[0].split()
number_of_letter = int(len(id_list)-1)
typ, data = mail_connection.fetch(id_list[number_of_letter], '(RFC822)')
raw_mail = data[0][1]

# Get subject from the last letter
last_mail=email.message_from_bytes(raw_mail)
subject = last_mail.get('Subject')
h = email.header.decode_header(subject)
letters_subject = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]

# Compare subject of letter that we have sent with this subject
assert(letters_subject == subject)






