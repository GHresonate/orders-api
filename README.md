# orders-api
```
In progress
```
A small Python api and helm chart for it. Still in progres, because I need to figure out how to run sql script to prepare database before deployment the better way.
## What needs to be done?
1) Add a way to run database_init.sql in the begining of deployment, maybe make run manual but by only one click of a button;

## How to setup this api?
1) git clone git@github.com:GHresonate/orders_api.git
2) create postgres database in a way you like it, and run database_init.sql for this db
3) add string to connect to database in secret file, in a format like the commented line in this file, but in base64
4) helm 
