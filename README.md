# TeamUp
A flask web app for forming balanced teams in educational settings


## Requirements

- Python3
- MySQL
	- Create a database named **team_building_tool**
	- See [teambuildingtool.sql](teambuildingtool.sql) and the tables below for details
	- Configure connectdb() in functions.py to connect to this database
- An email account for development
	- Set app.config variables in teamup.py to connect to this account

Libraries and Frameworks:
`$ pip install Flask`
`$ pip install Flask-Mail`
`$ pip install hashlib`
`$ pip install matplotlib`
`$ pip install pandas`
`$ pip install SQLAlchemy`


## Files and folders

teamup.py is the main flask app
functions.py contains the functions for the app
algorithm.py contains the primary algorithm
HTML files are found in the *templates* folder
Static files (CSS and images) are found in the *static* folder

## Database

**Students** table:
| student_id | class_id | username | password | name | analyst | diplomat | leader | explorer | group_no | skill1 | skill2 | skill3 | skill4 | 
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| int | varchar | varchar | varchar | varchar | int | int | int | int | int | int | int | int | int |

**Teachers** table:
| teacher_id | username | password | 
|--|--|--|
| int | varchar | varchar |

**Class** table:
| class_id | class_name | teacher_id | skill1 | skill2 | skill3 | skill4 | team_size | class_size |
|--|--|--|--|--|--|--|--|--|
| varchar | varchar | int | varchar | varchar | varchar | varchar | int | int | int |
