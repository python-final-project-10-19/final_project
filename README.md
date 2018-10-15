# Book Share Pro

[Trello Project Management Board](https://trello.com/b/NCEfqRZA/book-dating-app-project)

## Application Summary
TBD

## Quick Start
1. Clone this repository.
1. In the terminal, run ```cd final_project```
1. Run ```touch .env```
1. In the .env file, paste the appropriate environment variables (ask a team member).
1. In a separate terminal instance, run ```psql```
1. Run ```CREATE DATABASE book_share;```
1. Back in the main terminal instance, run ```pipenv shell```
1. Run ```pipenv install```
1. Run ```./manage.py makemigrations```
1. Run ```./manage.py migrate```
1. Run ```./manage.py createsuperuser``` and follow the steps.
1. Run ```./manage.py runserver```
1. In your browser, navigate to ```localhost:8000/admin/``` and login with superuser credentials.
1. Under ```Sites``` click on ```Sites```
1. In the upper right, click on ```Add site +```
1. In the domain name field, type ```localhost:8000```. In the Display Name field, type ```Books Share```. Click ```Save```. On the top left, navigate back to ```Home```
1. On the admin console Home page, under ```Social Accounts```, click on ```Social Applications```. On this page, click on ```Add social application +```.
1. Under the provider dropdown, choose ```Facebook```.
1. In the ```Name``` field, type ```Books Share```.
1. In the ```Client id``` and ```Secret key``` fields, type in the App ID and App Secret from this app on ```https://developers.facebook.com/```
1. In the ```Sites``` field, select ```localhost:8000``` and click on the right arrow so it appears under ```Chosen sites```. Then click ```Save```.
1. Logout from the admin console.
1. Navigate to ```localhost:8000```.
1. Login using FB Oauth.

## Database Schema
TBD

### Authors:
- Andrew Baik
- Ben Hurst
- Liz Mahoney test test
- Roman Kireev
</br>
Verion 0.0.0
</br>
