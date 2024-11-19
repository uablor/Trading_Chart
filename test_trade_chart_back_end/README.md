## Start project

run : pip install -r requ.txt

## start redis server
# run redis server in  port 127.0.0.1:6379
run : redis-server 


## start Socket server

run : daphne -p 9000 Core.asgi:application

## start Project

run : python manage.py runserver
