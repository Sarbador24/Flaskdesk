# Flaskdesk

Flaskdesk is a support ticketing system that helps you manage customer inquiries. It also provides all the context you need to resolve issues and allows you to categorize, prioritize, and assign customer tickets.

## Prerequisites

* Python 3.6+

## Installation

These instructions will get you a copy of the project up and running on your local machine.

1. Git clone or download the project files
```
git clone https://github.com/hazzillrodriguez/Flaskdesk.git

cd Flaskdesk
```

2. Create and activate the virtual environment then install requirements
```
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```

3. Set the environment variables
```
export FLASK_APP=run.py
export FLASK_ENV=development
```

4. Run migrations
```
flask db init
flask db migrate
flask db upgrade
```

5. Run the following commands to create an `admin account` and `seeds` to be inserted into the database
```
python create_admin.py
python seeds.py
```

### Update Configuration Settings

Before you can use this application, you will have to configure your email account and password that will be used to send `password reset` emails.

Instead of editing `config.py` and checking in sensitive information into the code repository, these settings can be set using OS environment variables in your `.bashrc` or `.bash_profile` shell configuration file.
```
export EMAIL_USER = 'you_email@example.com'
export EMAIL_PASS = 'your_password'
```
> If you are using a Google SMTP server, you must enable ***Less secure app access*** on your account.

6. Start the development web server:
```
flask run
```

You should then be able to view the application in the browser. To access the admin section, login with:

Username: admin@flaskdesk.com

Password: flaskdesk

## License

Distributed under the MIT License. See `LICENSE` for more information.