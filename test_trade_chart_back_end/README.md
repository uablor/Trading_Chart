


# install requirements.txt 
# use everytime push to git

run : pip freeze > requirements.txt

# install virtualenv 

run : pip install virtualenv

# install .venv

run : virtualenv .venv

# use .venv

run : . .venv/Scripts/activate || ro || source .venv/Scripts/activate

## Start project

run : pip install -r requ.txt

## migrate you modal 
 run : python manage.py migrations
 and run : python manage.py migrate

## start redis server
# run redis server in  port 127.0.0.1:6379 here for shutdown redis-cli shutdown
run : redis-server 


## start Socket server

run : daphne -p 9000 Core.asgi:application

## start Project

run : python manage.py runserver
