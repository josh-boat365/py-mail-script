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

## How to run
```python app.py```

