import os
import csv
import time
import threading 
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

# define email messages for each role and experience level
email_messages = {
    'frontend': {
        '<3': roles_types()['frontend']['requirements'] + roles_types()['frontend']['experience_levels']['years_of_experience < 3'],
        '3-5': roles_types()['frontend']['requirements'] + roles_types()['frontend']['experience_levels']['years_of_experience < 5'],
        '>5': roles_types()['frontend']['requirements'] + roles_types()['frontend']['experience_levels']['years_of_experience >= 5']
    },
    'backend': {
        '<3': roles_types()['backend']['requirements'] + roles_types()['backend']['experience_levels']['years_of_experience < 3'],
        '3-5': roles_types()['backend']['requirements'] + roles_types()['backend']['experience_levels']['years_of_experience < 5'],
        '>5': roles_types()['backend']['requirements'] + roles_types()['backend']['experience_levels']['years_of_experience >= 5']
    },
    'fullstack': {
        '<3': roles_types()['fullstack']['requirements'] + roles_types()['fullstack']['experience_levels']['years_of_experience < 3'],
        '3-5': roles_types()['fullstack']['requirements'] + roles_types()['fullstack']['experience_levels']['years_of_experience < 5'],
        '>5': roles_types()['fullstack']['requirements'] + roles_types()['fullstack']['experience_levels']['years_of_experience >= 5']
    }
}

# function to send email
def sendEmail(name, email, role, years_of_experience, delay):
    with app.app_context():
        msg = Message()
        msg.subject = "Invitation to Slightly Techie Network"
        msg.sender = ("Slightly Techie", "casvalabs@gmail.com" )
        msg.recipients = [email]
        msg.cc =  ['slightlytechie@gmail.com', 'wellingtoncharlottenaaodarley@gmail.com','bquansah007@gmail.com','etiboah@gmail.com','kwame.nyarko365@gmail.com']
        if role in email_messages:
            if years_of_experience < 3:
                msg.html = render_template('email.html', recipient_name=name, role=role, message=email_messages[role]['<3'])
            elif years_of_experience in range(3, 6):
                msg.html = render_template('email.html', recipient_name=name, role=role, message=email_messages[role]['3-5'])
            elif years_of_experience > 5:
                msg.html = render_template('email.html', recipient_name=name, role=role, message=email_messages[role]['>5'])
            else:
                msg.html = render_template('email.html', recipient_name=name, message="Sorry.., we are experiencing some technical difficulties. we will get back to you shortly.")
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
    


# function to get name, email, role and years_of_experience from csv file
def read_csv(filename):
    rows = []
    try:
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append((row['Name'], row['Email'], row['Role'], int(row['Years_of_experience'])))
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except ValueError:
        print(f"Invalid value in CSV file: {filename}")

    return rows


#function to send email to multiple persons at the same time on a different thread  
def send_emails_to_respective_persons():
    name_email_pairs = read_csv('emails.csv')  #[('Joshua Nyarko Boateng', 'test1@gmail.com', 'backend', '8'), ('Kwame Kay', 'test2@gmail.com', 'fullstack', '1'), ('krypton', 'test3@gmail.com', 'frontend', '12')]
    delay = 0
    num_of_emails_sent = 0
    threads = []

    # def send_email_wrapper(name, email, role, years_of_experience, delay):
    #     time.sleep(delay)
    #     sendEmail(name, email, role.lower(), int(years_of_experience), delay)

        

    for name, email, role, years_of_experience in name_email_pairs:
        thread = threading.Thread(target=sendEmail, args=(name, email, role.lower(), int(years_of_experience), time.sleep(delay)))
        threads.append(thread)
        thread.start()
        num_of_emails_sent += 1
        delay += 1
        print(f"Sent {num_of_emails_sent} emails in {delay} seconds")

    for thread in threads:
        thread.join()
    
    print(f"Number of Threads = {len(threads)}")

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
            return f"ValueError:,{e} "
        except Exception as exp:
            print('An Error Occured!!: ', exp)
            return f" An Error Occured !!:,{exp} "
        finally:
            return "Mail Sent!!"
        

        
       
    return render_template('index.html')

@app.route('/email')
def mailTemplate():
    return render_template('email.html')


if __name__ == '__main__':
    app.run(debug=True)

