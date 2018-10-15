# Book Share Pro

[Trello Project Management Board](https://trello.com/b/NCEfqRZA/book-dating-app-project)

## Application Summary
TBD

## Quick Start
1. Clone this repository.
2. In the terminal, run ```cd final_project```
3. In a separate terminal instance, run ```psql```
4. Run ```CREATE DATABASE book_share;```
5. Back in the main terminal instance, run ```pipenv shell```
6. Run ```pipenv install```
7. Run ```./manage.py makemigrations```
8. Run ```./manage.py migrate```
9. Run ```./manage.py createsuperuser``` and follow the steps.
10. Run ```./manage.py runserver```
11. In your browser, navigate to ```localhost:8000/admin/``` and login with superuser credentials.
12. Under ```Sites``` click on ```Sites```
13. In the upper right, click on ```Add site +```
14. In the domain name field, type ```localhost:8000```. In the Display Name field, type ```Books Share```. Click ```Save```. Navigate back to ```Home```
15. On the admin console Home page, under ```Social Accounts```, click on ```Social Applications```. On this page, click on ```Add social application +```.
16. Under the provider dropdown, choose ```Facebook```.
17. In the ```Name``` field, type ```Books Share```.
18. In the ```Client id``` and ```Secret key``` fields, type in the App ID and App Secret from this app on ```https://developers.facebook.com/```
19. In the ```Sites``` field, select ```localhost:8000``` and click on the right arrow so it appears under ```Chosen sites```. Then click ```Save```.
20. Logout from the admin console.
21. Navigate to ```localhost:8000```.
22. Login using FB Oauth.

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
