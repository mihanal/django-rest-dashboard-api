
# Django Dashboard Rest APIs 

A set of dashboard Restful APIs written in Django for basketball league

## Technologies used
- Django
- DRF
- sqlite

## Versions
- Python : 3.8.6

## Running the Application

Create the DB tables first:

`$ python manage.py makemigrations` \
`$ python manage.py migrate`

Load initial data:

`$ python manage.py load_data`

Start the application:

`$ python manage.py runserver`

## API Reference

| Endpoint | HTTP Method     | Result                |
| :-------- | :------- | :------------------------- |
| `/league/players` | `GET` | List of players in the league |
| `/league/players/:id` | `GET` | Player Details |
| `/league/teams` | `GET` | List of teams in the league |
| `/league/teams/:id` | `GET` | Team Details |
| `/league/teams/:id/players` | `GET` | Players in a team |
| `/league/teams/<int:id>/average` | `GET` | Above average players |
| `/league/games/` | `GET` | League games  |

