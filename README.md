# orders-api
Ready to deploy orders-api. Written in Python with FastApi and SQLAlchemy, and prepared for deploy to a kubernetes cluster with Helm chart.

For easyer deployment I need to figure out how to run sql script to prepare database before deployment the better way.
For production secret must be changed, because for now that is absolutly 'unsecret', and it would be better to add something like aws secret store with real encryption.
## What needs to be done?
1) Add a way to run database_init.sql in the begining of deployment, maybe make run manual but by only one click of a button;

## How to setup this api?
1) ```git clone git@github.com:GHresonate/orders_api.git```
2) Create postgres database in a way you like it, and run database_init.sql for this db
3) Add database credentials in secrets.yaml file, in a format like the commented line in this file, but in base64
4) Connect to your Kubernetes cluster
5) ```kubectl create namespace orders-api```
6) ```helm install api helm --values helm/values_dev.yaml```
