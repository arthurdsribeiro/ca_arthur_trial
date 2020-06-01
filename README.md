![Django CI](https://github.com/arthurdsribeiro/ca_arthur_trial/workflows/Django%20CI/badge.svg?branch=master)

# Arthur Ribeiro's project of Consumer Affairs trial period.

ca_arthur_trial is a set of REST services to create reviews as a logged in user to custom companies.

## Requirements

- Python 3

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies
of the project and run it on your machine.

- `git clone`
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

(Note [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) is very optional but may make life considerably easier)

## Database setup

Before you run the application, please set up the database entities necessary to store the submitted reviews informations using the command:

`python manage.py migrate`

It's also important to mention that we have an admin view and in order to use it we have to create a *super user*, to do that, run:

`python manage.py createsuperuser`

Once you fill in all the required information you're all set to run the project.

## Running the project

After installing the dependencies and setting up the database and super user, run the application with the command:

`python manage.py runserver`

You'll be able to login to the admin website by navigating into `http://localhost:8000/admin/`

## Running unit tests

We have unit tests for all the REST services and for serialzers and models that compose the application, to run the test suite, just do:

`python manage.py test`

## Contributing

Since this is a project to be evaluated by Consumer Affairs we're not accepting pull requests or editions to the current codebase.


