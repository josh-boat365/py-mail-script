import os
import pandas as pd
from threading import Thread
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET'] = os.environ.get('APP_SECRET')

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') 
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT') 
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') 
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
app.config['NAME_EMAIL_PAIRS'] = os.environ.get('NAME_EMAIL_PAIRS')

mail = Mail(app)

# function to loop through pairs of names and emails
# def loop_through_name_email_pairs(name_email_pairs):
#     name_email_pairs = []
#     for name, email in name_email_pairs:
#         return name, email

#function to send email
def sendEmail(name, email):
    msg = Message()
    msg.subject = "Invitation to Slightly Techie Network"
    msg.sender = ("Slightly Techie","noreply@gmail.com")
    msg.recipients = [email]
    msg.html = render_template('email.html', recipient_name = name)
    mail.send(msg)

#function to send email to multiple persons at the same time on a different thread        
def send_emails_to_respective_persons():
    name_email_pairs = app.config['NAME_EMAIL_PAIRS']
    # name_email_pairs = [("Jane Doe","janedoe@gmail.com"),("John Doe","johndoe@gmail.com")] a list of name and email pairs

    # a loop to get the name and email of each person from the list 'name_email_pairs'
    for name, email in name_email_pairs:
        # name and email are passed to the thread, making use of the sendEmail function, so that the thread can send the email to respective persons
        thread = Thread(target=sendEmail(name=name,email=email))
        # the thread is started
        thread.start()
        # the thread in process is joined to the main thread until it is finished
        thread.join()





@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        send_emails_to_respective_persons()
        
        return "Mail Sent!!"
        
       
    return render_template('index.html')

@app.route('/email')
def mailTemplate():
    return render_template('email.html')


if __name__ == '__main__':
    app.run(debug= True)

