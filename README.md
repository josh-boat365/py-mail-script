# py-mail-script
This is a python script to send emails to multiple users using threading to send emails to respective persons 

## Usage
Install the following to run the script

```
pip install 
pip flask 
pip flask-mail 
pip python-dotenv
```

## App Config
> Create a ```.env``` file in the root folder to set the configuration for mail script.

> This is how your ```.env``` file should look like
``` 
APP_SECRET = 'Generate random characters for your application key'

MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = test@gmail.com
MAIL_PASSWORD = Test123


# whiles mail is being sent copy these mails
COPY_TO_MAILS=['test1@gmail.com', 'test2@gmail.com','test3@gmail.com','test4@gmail.com','test5@gmail.com']
```

> ## How to set up gmail smtp
1. Sign in to your Gmail Account
2. Search for ***App Passwords*** and click on it to open a tab.
3. Select ***Mail*** from the ***Select app*** dropdown.
4. Select ***Other(Custom name)*** from the ***Select device*** dropdown.
5. Give a name to the App (ex. ***Mail Script***)
6. Click on Generate to get password to be used for the Mail Script App.
7. To use your Gmail Account in third-party apps and testing purposes :
Mail: mygmailaccount@gmail.com
Password: Generated app password from gmail. 

## How to run
```python app.py```

