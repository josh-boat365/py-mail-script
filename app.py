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

def roles_types():
    years_of_experience = 0
    return   {'frontend':{
        years_of_experience < 3 : """
       Create a post webapp that: \n
       - Allows a user to create, view one, view all, update and delete a posts. \n
       - Push to Github and add interviewer as a collaborator. \n
       - Deploy on any platform of your choice and share link. \n
       - No need for backend or database, store data anyhow you see fit. \n""",
       years_of_experience >3 and years_of_experience < 5 : """
       Create a post webapp that: \n
       - Allows a user to create, view one, view all, update and delete a posts. \n
       - Push to Github and add interviewer as a collaborator. \n
       - Deploy on any platform of your choice and share link. \n
       - No need for backend or database, store data anyhow you see fit.
       - UI should be responsive(should work on mobile devices). \n
       - Add simple documentation on how to setup and run the app. \n""",
       years_of_experience > 5 : """
       Create a post webapp that: \n
       - Allows a user to create, view one, view all, update and delete a posts. \n
       - Push to Github and add interviewer as a collaborator. \n
       - Deploy on any platform of your choice and share link. \n
       - No need for backend or database, store data anyhow you see fit.
       - UI should be responsive(should work on mobile devices). \n
       - Add simple documentation on how to setup and run the app. \n
       - UX should be taken into consideration. \n
       - Setup unit test to cover at least 50% of the code. \n"""},
       'backend':{
        years_of_experience < 3 : """
       Create a post API that: \n
       - Allows a user to create, view one, view all, update and delete a posts. \n
       - Push to Github and add interviewer as a collaborator. \n
       - Deploy on any platform of your choice and share link. \n""", 
       years_of_experience >3 and years_of_experience < 5 : """
       Create a post API that: \n
       - Allows a user to create, view one, view all, update and delete a posts. \n
       - Push to Github and add interviewer as a collaborator. \n
       - Deploy on any platform of your choice and share link. \n\n
       - Add simple documentation on how to setup and run the app. \n""",
       years_of_experience > 5 : """
       Create a post API that: \n
       - Allows a user to create, view one, view all, update and delete a posts. \n
       - Push to Github and add interviewer as a collaborator. \n
       - Deploy on any platform of your choice and share link. \n\n
       - Add simple documentation on how to setup and run the app. \n
       - Dockerize solution. \n
       - Setup unit test to cover at least 50% of the code. \n"""},
         'fullstack':{
            years_of_experience < 3 : """
         Create a post webapp + API: \n
         - Allows a user to create, view one, view all, update and delete a posts \n.
         - Push to Github and add interviewer as a collaborator (two separate repos) \n.
         - Deploy on any platform of your choice and share link.\n 
         """,
         years_of_experience >3 and years_of_experience < 5 : """
          Create a post webapp + API: \n
         - Allows a user to create, view one, view all, update and delete a posts \n.
         - Push to Github and add interviewer as a collaborator (two separate repos) \n.
         - Deploy on any platform of your choice and share link.\n
         - Users should be able to authenticate and do these actions on only posts they created. \n
         - Add simple documentation on how to setup and run the app. \n """,
         years_of_experience > 5 : """
         Create a post webapp + API: \n
         - Allows a user to create, view one, view all, update and delete a posts \n.
         - Push to Github and add interviewer as a collaborator (two separate repos) \n.
         - Deploy on any platform of your choice and share link.\n
         - Users should be able to authenticate and do these actions on only posts they created. \n
         - Add simple documentation on how to setup and run the app. 
         - Dockerize solution both webpp and api. \n
         - Setup unit test to cover at least 50% of the code. \n"""},
       }

#function to send email
def sendEmail(name, email, role, years_of_experience):
    roles_types()
    #frontend messages roles
    frontend_junior = roles_types()['frontend'][years_of_experience < 3]
    frontend_intermediate = roles_types()['frontend'][years_of_experience > 3 and years_of_experience < 5]
    frontend_senior = roles_types()['frontend'][years_of_experience > 5]

    #backend messages roles
    backend_junior = roles_types()['backend'][years_of_experience < 3]
    backend_intermediate = roles_types()['backend'][years_of_experience > 3 and years_of_experience < 5]
    backend_senior = roles_types()['backend'][years_of_experience > 5]

    #fullstack messages roles
    fullstack_junior = roles_types()['fullstack'][years_of_experience < 3]
    fullstack_intermediate = roles_types()['fullstack'][years_of_experience > 3 and years_of_experience < 5]
    fullstack_senior = roles_types()['fullstack'][years_of_experience > 5]
    
    msg = Message()
    msg.subject = "Invitation to Slightly Techie Network"
    msg.sender = ("Slightly Techie","noreply@gmail.com")
    msg.recipients = [email]
    if role == 'frontend':
        if years_of_experience < 3:
            msg.html = render_template('email.html', recipient_name = name, message = frontend_junior)
            mail.send(msg)
            pass
        elif years_of_experience >=3 and years_of_experience <=5:
            msg.html = render_template('email.html', recipient_name = name, message = frontend_intermediate)
            mail.send(msg)
            pass
        elif years_of_experience > 5:
            msg.html = render_template('email.html', recipient_name = name,  message = frontend_senior)
            mail.send(msg)
            pass
    if role == 'backend':
        if years_of_experience < 3:
            msg.html = render_template('email.html', recipient_name = name, message = backend_junior)
            mail.send(msg)
            pass
        elif years_of_experience >=3 and years_of_experience <=5:
            msg.html = render_template('email.html', recipient_name = name, message = backend_intermediate)
            mail.send(msg)
            pass
        elif years_of_experience > 5:
            msg.html = render_template('email.html', recipient_name = name, message = backend_senior)
            mail.send(msg)
            pass
    if role == 'fullstack':
        if years_of_experience < 3:
            msg.html = render_template('email.html', recipient_name = name, message = fullstack_junior)
            mail.send(msg)
            pass
        elif years_of_experience >=3 and years_of_experience <=5:
            msg.html = render_template('email.html', recipient_name = name, message = fullstack_intermediate)
            mail.send(msg)
            pass
        elif years_of_experience > 5:
            msg.html = render_template('email.html', recipient_name = name, message = fullstack_senior)
            mail.send(msg)
            pass
        else:
            msg.html = render_template('email.html', recipient_name = name, message = "Sorry.., we are experiencing some technical difficulties. we will get back to you shortly.")
            mail.send(msg)  


#function to send email to multiple persons at the same time on a different thread        
def send_emails_to_respective_persons():
    name_email_pairs = [
     ("Jane Doe" ,"janedoe@gmail.com", "frontend", 3),("John Doe", "johndoe@gmail.com", "backend", 2)
]
    # name_email_pairs = [("Jane Doe","janedoe@gmail.com"),("John Doe","johndoe@gmail.com")] a list of name and email pairs
    threads = [] # a list to hold the threads

    # a loop to get the name and email of each person from the list 'name_email_pairs'
    for name, email, role, years_of_experience in name_email_pairs:
        # name and email are passed to the thread, making use of the sendEmail function, so that the thread can send the email to respective persons
        thread = Thread(target=sendEmail(name=name,email=email, role=role, years_of_experience=years_of_experience))
        # the thread is started
        thread.start()
        # the thread in process is added to the list of finished threads
        threads.append(thread)
    


    for thread in threads:
        # the threads are joined to help the main thread wait for the threads to finish before the end of this script
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

