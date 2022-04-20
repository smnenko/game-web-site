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
> Example:   
>
> SECRET_KEY=mscb#cvbrtrtsxzcz#x*aw1@nrft#nnrtf95t#ndd0az^+  
> DATABASE_NAME=game-web-site  
> DATABASE_USER=postgres  
> DATABASE_PASS=postgres  
> DATABASE_HOST=localhost  
> DATABASE_PORT=5432  
>
> You also need to create PostgreSQL database with DATABASE_NAME that you filled  

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
![Main](https://raw.githubusercontent.com/smnenko/gamemuster/master/docs/images/Main%20page.png)
* Login page
![Login](https://raw.githubusercontent.com/smnenko/gamemuster/master/docs/images/Login%20page.png)
* Signup page
![Signup](https://raw.githubusercontent.com/smnenko/gamemuster/master/docs/images/Signup%20page.png)
* Profile page
![Profile](https://raw.githubusercontent.com/smnenko/gamemuster/master/docs/images/Profile%20page.png)
* Musts page
![Musts](https://raw.githubusercontent.com/smnenko/gamemuster/master/docs/images/Musts%20page.png)
* Game page
![Game](https://raw.githubusercontent.com/smnenko/gamemuster/master/docs/images/Game%20page.png)
