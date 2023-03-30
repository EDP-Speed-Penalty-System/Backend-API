
## Software Requirements

* Python 
* Git

### Setting up environment

* Create a virtual environment  
  * on **Ubuntu**: `python3 -m venv env`  
  * on **Windows PowerShell**: `python -m venv env`
* Activate the *env*    
  * on **Ubuntu**: `source env/bin/activate`
  * on **Windows PowerShell**: `.\env\Scripts\Activate.ps1`     
  **Note** : On Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following command: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
* Install the requirements: `pip install -r requirements.txt`

### Running server

* Run the server `python manage.py runserver`

  
### Migrating Changes (Database)

* Make migrations `$ python manage.py makemigrations`  
* Migrate the changes to the database `$ python manage.py migrate`


