# UksGitHub
UksGitHub is a web-based version-control and collaboration platform for software developers.

### Contributors (Team 2):
|  | Student |
| ------ | ------ |
| Student 1 | Kristina Đurić E2 92/2021| 
| Student 2 | Maja Dragojlović E2 95/2021| 
| Student 3 | Milena Kovačević E2 117/2021|
| Student 4 | Branislav Dobrokes E2 30/2021|
| Student 5 | Marija Milanović E2 98/2021|


### Instructions
1. Open a terminal as admin and create a virtual environment <br>
```
python -m venv <envName>
```
2. Afterwards, activate created virtual environment
   - For Linux: 
    ```
    source env/bin/active
    ```
   - For Windows:
     ```
     env\Scripts\activate.bat
     ```
3. To deactivate virtual environment type
```
deactivate
```
4. Install the necessary dependencies
```
pip3 install -r requirements.txt
```
5.  Make migrations, create super user and run the application
```
cd Uks
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Technologies:
- Python (Django REST Framework)
- Docker
- Postgres

Diagram: https://app.diagrams.net/#G1IoR5kPiXvhx9p8mQcYWDl8o9Gzbv1dUL
