
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

## ER Diagram

![edp_erdiagram](https://github.com/EDP-Speed-Penalty-System/Backend-API/assets/111732396/b6986cf9-705a-4117-8eae-d4539360904c)

## Mobile App in execution



![image](https://github.com/EDP-Speed-Penalty-System/Backend-API/assets/111732396/43570633-8e6a-4aab-8e1a-2162c52bc62e)


![image](https://github.com/EDP-Speed-Penalty-System/Backend-API/assets/111732396/ac7b72cf-d924-4218-ba45-5bbb6a045c7a)


![image](https://github.com/EDP-Speed-Penalty-System/Backend-API/assets/111732396/89003ffe-c088-4611-bc99-3b5f4dfa0413)            


![image](https://github.com/EDP-Speed-Penalty-System/Backend-API/assets/111732396/d31ea35f-2222-447b-8d6c-1aaaf8fed9b8)


![image](https://github.com/EDP-Speed-Penalty-System/Backend-API/assets/111732396/f81d498c-d931-4add-9483-1d0ac13bbb9c)






 

