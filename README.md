# About 
I felt a very flexible approch would be best so the database is simply being used to store json objects
see the EER diagram: dtabase_eer_diagram.png

## Backend
I utilized flask + sqlalchemy deployed with zappa to a lambda for the api.
While i could have included the frontend I thought it would be better to host that in s3.

### Deployment overview
- set credentials in create_rds_db.sh and .env
- run create_rds_db.sh
- run zappa deploy
- ping <lambad endpoint>/build - creates the database tables

## Frontend
I went with vue.js + vue-bootstrap.
I created the app for configuring the risk types as well as the fields for each type.
The fields can be added removed and edited as well as previewed.
I added support for several field types.

### Deployment overview
- create s3 bucket for static hosting
- upload contents of frontend/dist to the bucket
