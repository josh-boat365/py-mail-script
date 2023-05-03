import os
import csv
import time
import threading as Thread
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET'] = os.environ.get('APP_SECRET')

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') 
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT') 
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') 
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
app.config['COPY_TO_MAILS'] = os.environ.get('COPY_TO_MAILS')


mail = Mail(app)


def roles_types():
    roles = {
        'frontend': {
            'requirements': [
                "Create a post webapp that:",
                "- Allows a user to create, view one, view all, update and delete a posts.",
                "Push to Github and reply to this email with a prompt",
                "- Deploy on any platform of your choice and share link.",
                "- No need for backend or database, store data anyhow you see fit."
            ],
            'experience_levels': {
                'years_of_experience < 3': [],
                'years_of_experience < 5': [
                    "- UI should be responsive (should work on mobile devices). ",
                    "- Add simple documentation on how to setup and run the app."
                ],
                'years_of_experience >= 5': [
                    "- UX should be taken into consideration.",
                    "- Setup unit test to cover at least 50% of the code."
                ]
            }
        },
        'backend': {
            'requirements': [
                "Create a post API that:", 
                "- Allows a user to create, view one, view all, update and delete a posts.", 
                "Push to Github and reply to this email with a prompt", 
                "- Deploy on any platform of your choice and share link."
            ],
            'experience_levels': {
                'years_of_experience < 3': [],
                'years_of_experience < 5': [
                    "- Add simple documentation on how to setup and run the app."
                ],
                'years_of_experience >= 5': [
                    "- Dockerize solution.",
                    "- Setup unit test to cover at least 50% of the code."
                ]
            }
        },
        'fullstack': {
            'requirements': [
                "Create a post webapp + API:",
                "- Allows a user to create, view one, view all, update and delete a posts.",
                "Push to Github and reply to this email with a prompt (two separate repos).",
                "- Deploy on any platform of your choice and share link."
            ],
            'experience_levels': {
                'years_of_experience < 3': [],
                'years_of_experience < 5': [
                    "- Users should be able to authenticate and do these actions on only posts they created.",
                    "- Add simple documentation on how to setup and run the app."
                ],
                'years_of_experience >= 5': [
                    "- Users should be able to authenticate and do these actions on only posts they created.",
                    "- Add simple documentation on how to setup and run the app.",
                    "- Dockerize solution both webapp and API.",
                    "- Setup unit test to cover at least 50% of the code."
                ]
            }
        }
    }
    return roles

#function to send email
def sendEmail(name, email, role, years_of_experience, delay):
    roles_types()
    #frontend messages roles
    frontend_junior = roles_types()['frontend']['requirements'] + roles_types()['frontend']['experience_levels']['years_of_experience < 3']
    frontend_intermediate = roles_types()['frontend']['requirements'] + roles_types()['frontend']['experience_levels']['years_of_experience > 3 and years_of_experience < 5']
    frontend_senior = roles_types()['frontend']['requirements'] + roles_types()['frontend']['experience_levels']['years_of_experience > 5']

    #backend messages roles
    backend_junior = roles_types()['backend']['requirements'] + roles_types()['backend']['years_of_experience < 3']
    backend_intermediate = roles_types()['backend']['requirements'] + roles_types()['backend']['experience_levels']['years_of_experience > 3 and years_of_experience < 5']
    backend_senior = roles_types()['backend']['requirements'] + roles_types()['backend']['experience_levels']['years_of_experience > 5']

    #fullstack messages roles
    fullstack_junior = roles_types()['fullstack']['requirements'] + roles_types()['fullstack']['experience_levels']['years_of_experience < 3']
    fullstack_intermediate = roles_types()['fullstack']['requirements'] + roles_types()['fullstack']['experience_levels']['years_of_experience > 3 and years_of_experience < 5']
    fullstack_senior = roles_types()['fullstack']['requirements'] + roles_types()['fullstack']['experience_levels']['years_of_experience > 5']
     
    with app.app_context():
        msg = Message()
        msg.subject = "Invitation to Slightly Techie Network"
        msg.sender = ("Slightly Techie", "casvalabs@gmail.com" )
        msg.recipients = [email]
        msg.cc =  app.config['COPY_TO_MAILS']
        if role == 'frontend':
            if years_of_experience < 3:
                msg.html = render_template('email.html', recipient_name = name, role = 'frontend', message = frontend_junior)
                mail.send(msg)

            elif years_of_experience in range(3,6):
                msg.html = render_template('email.html', recipient_name = name, role = 'frontend', message = frontend_intermediate)
                mail.send(msg)
                
            elif years_of_experience > 5:
                msg.html = render_template('email.html', recipient_name = name, role = 'frontend', message = frontend_senior)
                mail.send(msg)
                
        if role == 'backend':
            if years_of_experience < 3:
                msg.html = render_template('email.html', recipient_name = name, role = 'backend', message = backend_junior)
                mail.send(msg)
                
            elif years_of_experience in range(3,6):
                msg.html = render_template('email.html', recipient_name = name, role = 'backend', message = backend_intermediate)
                mail.send(msg)
                
            elif years_of_experience > 5:
                msg.html = render_template('email.html', recipient_name = name, role = 'backend', message = backend_senior)
                mail.send(msg)
            
        if role == 'fullstack':
            if years_of_experience < 3:
                msg.html = render_template('email.html', recipient_name = name, role = 'fullstack', message = fullstack_junior)
                mail.send(msg)
                
            elif years_of_experience in range(3,6):
                msg.html = render_template('email.html', recipient_name = name, role = 'fullstack', message = fullstack_intermediate)
                mail.send(msg)
                
            elif years_of_experience > 5:
                msg.html = render_template('email.html', recipient_name = name, role = 'fullstack', message = fullstack_senior)
                mail.send(msg)
                
            else:
                msg.html = render_template('email.html', recipient_name = name, message = "Sorry.., we are experiencing some technical difficulties. we will get back to you shortly.")
                mail.send(msg)  

# send reminder mail 
def sendEMailReminder(name, email):
    reminderDate = "January 9th"
    reminder =[ "I hope you had a great holiday season! Just a quick note to remind you about the coding challenge to join the Slightly Techie Network.",
    f"The deadline for submission is {reminderDate}. Kindly treat this with top priority and submit your work on time. Please keep in mind submitting the task is a requirement for joining the network.",
    "Wishing you the best of luck, happy coding!",
    "Best Regards,",
    "Joshua"]

    msg = Message()
    msg.subject = "Reminder!! - Invitation to Slightly Techie Network"
    msg.sender = ("Slightly Techie","casvalabs@gmail.com")
    msg.recipients = [email]
    msg.cc = app.config['COPY_TO_MAILS']
    msg.html = render_template('reminder.html', recipient_name = name,  message = reminder)
    mail.send(msg)
    

# function to get name,email,role and years_of_experience from csv file
def read_csv(filename):
  rows = []
  with open(filename, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      rows.append((row['Name'],
      row['Email'],
      row['Role'],
      row['Years_of_experience'] ))
    return rows


#function to send email to multiple persons at the same time on a different thread  
      
def send_emails_to_respective_persons():
    name_email_pairs = [('Jerry Wilson', 'wilsonjerry182@gmail.com', 'backend', '1')] #read_csv('emails.csv') #[('Joshua Nyarko Boateng', 'test1@gmail.com', 'backend', '8'), ('Kwame Kay', 'test2@gmail.com', 'fullstack', '1'), ('krypton', 'test3@gmail.com', 'frontend', '12')]
                        
    delay = 0
    num_of_emails_sent = 0
    Threads = []
    # a loop to get the name and email of each person from the list 'name_email_pairs'
    for name, email, role, years_of_experience in name_email_pairs:
        # name, email, role, years_of_experience are passed to the thread, making use of the sendEmail function, so that the thread can send the email to respective persons
        # years = int(years_of_experience)
        # r = role.lower()
        # sendEmail(name,email,r,years,time.sleep(delay))
        thread = Thread.Timer(delay, sendEmail, args=[name,email, role.lower(),int(years_of_experience), delay])
        # # # the thread is started
        thread.start()
        Threads.append(thread)

        num_of_emails_sent += 1
        delay += 1
        print(f"Sent {num_of_emails_sent} emails in {delay} seconds")

    for threadd in Threads:
        threadd.join()
    print(f"Number of Threads = {len(Threads)}")
        
def send_reminder_email():
    name_email_pairs = read_csv('reminder_emails.csv')
    reminderMailsSent = 0
    for name, email in name_email_pairs:
        sendEMailReminder(name,email)
        reminderMailsSent += 1
        
    print("Number of Reminder Emails Sent: ", reminderMailsSent)


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':

        try:
            send_emails_to_respective_persons()
            #send_reminder_email()
        except ValueError as e:
            print('Error: ', e)
        except Exception as exp:
            print('An Error Occured!!: ', exp)
        finally:
            return "Mail Sent!!"
        

        
       
    return render_template('index.html')

@app.route('/email')
def mailTemplate():
    return render_template('email.html')


if __name__ == '__main__':
    app.run(debug=True)

