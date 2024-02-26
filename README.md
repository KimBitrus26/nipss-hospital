# NIPSS Hospital Mgt System


### Prequisites:
`
virtual environment,
python3

`

### Preparing your project

- Create a Folder on your Local machine / Computer
- Open Command prompt(git bash) / Terminal in the same folder location

### Cloning the Repository

Visit the project Repository on Github Website: 

- Click on the "Code" button on the Repo page

- Copy the URL  

- In your Terminal, run: git clone repo-url-here

### Creating a virtual environment (for gitbash users)

- run: python -m venv venv (Note i assemed you virtualenv installed.  venv is the name of your virtual environment in this case)
- run: source env/scripts/activate (To activate the virtual environment) or .venv/bin/activate


### Installing Django and other dependencies

- run: pip install -r requirements.txt

### Create a .env file to store environment variables in the same folder with manage.py file
- run: export $(xargs < .env)

### Run migration
- run: python3 manage.py makemigrations
- run: python3 manage.py migrate

### Running the server

- run: python3 manage.py runserver
