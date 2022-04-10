# djangoBack

Download this project and run the server. Eyeconic is the project name and 
Drone is the app name. following are the command to start the server. 
Navigate to the main folder and run the following command.

python manage.py runserver.

Once you run the server, it should start on  http://127.0.0.1:8000/

then hit the urls are required. The code is pretty much self explanatory. But i will explain the code to the team again once we integrate this. 

To resolve cors error, 
pip install django-cors-headers

In settings.py file,

MIDDLEWARE = [  
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

`CORS_ORIGIN_ALLOW_ALL = True`
