# GameMuster(game-web-site)
GameMuster is a web application that parse games and tweets from IGDB and Twitter.
### Installation
Create empty django-application and get **SECRET_KEY** from it
Clone repo from github using **git**
```
git clone https://github.com/smnenko/game-web-site.git
```
Configure python virtual environment (good practice) and run next command from root directory
```
pip install -r requirements.txt
```
Go to **.env** file and fill all fields
Run next commands in root directory (use python3 on linux os)
```
python manage.py migrate
python manage.py loaddata initial.json
python manage.py runserver
```
Go to *https://localhost:8000/* and be fine =)
##### Or you can start with docker-compose
> You need fill DATABASE_HOST to "db" (without quotes) after "=" and DATABASE_PORT to "5432" (without quotes) in .env file
```
docker-compose up --build
```
### Screenshots
* Main page
![Main](https://github.com/smnenko/game-web-site/blob/master/docs/images/Main%20page.PNG?raw=true)
* Login page
![Login](https://github.com/smnenko/game-web-site/blob/master/docs/images/Login%20page.PNG?raw=true)
* Signup page
![Signup](https://github.com/smnenko/game-web-site/blob/master/docs/images/Signup%20page.PNG?raw=true)
* Profile page
![Profile](https://github.com/smnenko/game-web-site/blob/master/docs/images/Profile%20page.PNG?raw=true)
* Musts page
![Musts](https://github.com/smnenko/game-web-site/blob/master/docs/images/Musts%20page.PNG?raw=true)
