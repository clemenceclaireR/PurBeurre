### **Purbeurre**

#### **Description**

This is the 8th project which has been developed for Openclassrooms.

#### **What does it do?**

It is a food substitute finder. Search for a product you like, and it will
display the same kind of products but with a better nutriscore.
If you're logged in, you can save the products which will retain 
your attention and browse it later in your saved products section.
You can of course 

#### **How to use ?** 

You have 2 options.

**1 - Heroku**

Just visit this link ! _https://rugged-badlands-94185.herokuapp.com/_

**2 - Cloning this repository**

**Prerequisites**  

*1) Python*

Install on Linux : 
1) With command line:
    
    
    apt install python3
2) Download compressed file here : https://www.python.org/downloads/source/ 

Install on Windows : Download here => https://www.python.org/downloads/windows/

Install on MacOS : Download here => https://www.python.org/downloads/mac-osx/

*2) PIP*

Install on windows : Download here => https://bootstrap.pypa.io/get-pip.py

*3) Postgres Database*



### Depencies
Install the dependencies with :


     pip install requirements.txt

### Environment
Configure your environment variable for this project. You'll need : 

***If production***

    ENV=production
    SECRET_KEY="mysecretkey",
    DB_PASSWORD="mydbpassword"


***If development***

Create a config.json file and place it in the project's root.
Write inside your environment variables in a dictionary format, like so:

    {
      "SECRET_KEY": "mysecretkey",
      "DB_PASSWORD":  "mypassword",
      "DB_USER":  "username",
      "DB_NAME":  "dbname",
      "DEBUG": "True"
    }

### Postgres database

**Install PostgreSQL**

This project is configured for a Postgres SQL database. If you want to use
another database, you'll have to change the settings in `settings.py` file.

Install on Linux (check for you distribution, here, it's working for Debian 10) :

    apt install postgresql-11 postgresql-client-11

Install on Windows : Download here => https://www.postgresql.org/download/windows/

Install on MacOS : Download here => https://www.postgresql.org/download/macosx/

**Create the database**

On your postgres server, create a database named "purbeurre" and a user
named "postgres".

### Run Migrations

In order to create the tables, run the following commands :


    python manage.py makemigrations
    python manage.py migrate
    
### Populate the database

    python manage.py api_openfoodfacts

### Launching
- Run the following commands in your terminal :


    python manage.py runserver
- Launch you web browser and go to the local server, _127.0.0.1:8000_ by default


### Testing with django test library

In order to run the tests, do like so :
- Go the the project's root in your terminal
- Runthe following command (coverage has to be installed - included in requirements.txt
file of this project) :


    coverage run manage.py test
    

You can test the coverage of the tests like so :

    coverage html

It will generate a _htmlcov_ directory in the project's root. Launch
_index.html_ in your browser to see the results.
