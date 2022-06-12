# Trivia API

![](C:\Users\Aboubakar Abba\Documents\Hyeldas\UDACITY\trivia_app\backend\Screenshot 2022-06-11 181812.png)

Trivia as the name implies is a knowledge testing API design to be simple to deploy and easy to use. Questions and their categories can be added with ease. There is also a quiz feature. The API is professionally built with the required features that are found in similar styled apps. It is a fully featured completely RESTful API

## Table of Contents

[TOC]


## Introduction



## Setting up the API

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.
### Database

The database engine used for the API is Postgres. Get more information on setup and configuration:

- [Windows](https://www.guru99.com/download-install-postgresql.html)
- [Linux/Ubuntu](https://linuxhint.com/install_postgresql_-ubuntu/)
- [MAC OS](https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql-macos/)

#### Set up the Database

- With Postgres running, create a `trivia` database using either of the following methods:
    1. Bash
        ```bash
        createdb trivia
        ```
    2. SQL (From the postgres shell)
        ```sql
        CREATE DATABASE trivia;
        ```
- Populate the database using the `trivia.psql` file provided. Use one of the two methods provided below:
    1. Using CLI/Bash - From the `backend` folder in terminal run:

        ```bash
        psql trivia < trivia.psql
        ```
    2. Inside Postgres shell, connect to the trivia database and input:
    	```bash
    	\i '/<complete_file_path>/trivia.psql'
    	```

### Run the Server

From within the app directory first ensure you are working using your created virtual environment. Add flask setup `FLASK_APP` `FLASK_DEV` `FLASK_DEBUG` with the corresponding values as environment variables.

e.g.
- In MAC OS/Linux `export FLASK_APP=<app_name>`
- In Windows PowerShell `$env:FLASK_APP = '<app_name>'` 

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Interacting with the API

### API Endpoints

###### Get categories

------

`GET '/api/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample Request
```bash
curl GET -X localhost:5000/api/categories
```
- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
###### Get questions

------

`GET '/api/questions'`

- Fetches a dictionary of categories and questions.  In the `categories`, the keys are the ids and the value is the corresponding string of the category. The `questions` key have a list of a maximum of ten question objects as the values. More questions could be accessed by providing the optional `page` query. Properties of the returned object include `current_category` `success` and `total_questions`  
- Request Arguments: `page` (optional)
- Sample Request 
```bash
curl GET -X localhost:5000/api/questions?page=1
```
- Response: An object with keys `categories` `questions` `current_category` `success` and `total_questions`.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 0,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },...],
  "success": true,
  "total_questions": 20
}
    
```
###### Create question

------

`POST '/api/questions'`

- Used to create a new question and add it to the database.

- Request Parameters: `question` `answer` `difficulty` `category`

  | Parameter  | Type                                                         |
  | ---------- | ------------------------------------------------------------ |
  | question   | String                                                       |
  | answer     | String                                                       |
  | difficulty | Number (1-10)                                                |
  | category   | Number (get from list of categories [here](#get-categories)) |

- Sample Request

  ```bash
  curl -i -X POST -H "Content-Type: application/json" \
  -d "{\"question\":\"What is the first month in the year?\",\
  	\"answer\":\"January\", \
  	\"difficulty\":1, \
  	\"category\":2}" 
  http://localhost:5000/api/questions
  ```

- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
    "success": True,
    "question": "What is the first month in the year?"
}
```
###### Search for Question(s)

`POST '/api/questions'`

- Fetches a dictionary containing the keys `current_category` `questions` `success` `total_questions`. The `questions` key has a list of questions marching the search term as values.

- Request Arguments: `searchTerm`

  | Parameter  | Type   |
  | ---------- | ------ |
  | searchTerm | String |

- Sample Request
```bash
  curl -i -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"lake\"}" \ 
  http://localhost:5000/api/questions
```

- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "current_category": 0,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
###### Delete a question

------

`DELETE '/api/questions/<question_id>'`

- Deletes a question that has an id identical to the `question_id` provided in the URL.

- Request Arguments: None

- Sample Request

  `curl -X DELETE localhost:5000/api/questions/1`

- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "success": True
}
```
###### Get questions belonging to a category

`GET '/api/categories/<category_id>/questions'`

- Fetches a dictionary with keys `current_category` `questions` `success`  and `total_questions`. The `questions` key contains a list of question objects that belong to the category with id provided in the URL as `category_id`

- Request Arguments: None

- Sample Request

```bash
curl -X GET localhost:5000/api/categories/5/questions
```

- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 			1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the 			role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

###### Start a quiz

------

`POST '/api/quizzes'`

- Starts a quiz session. It returns a random question based on the provided category. 

  > Note: The id of the answered questions should be appended to the `previous_questions` parameter for subsequent request after the first one

- Request Arguments: 

  | Parameter          | Type                                                         |
  | ------------------ | ------------------------------------------------------------ |
  | previous_questions | List ([] (first request) or [number, number] (subsequent requests)) |
  | quiz_category      | Dictionary ( `{id: Number, type: "category_name"}`)          |

- Sample Request

  ```bash
   curl -i -X POST -H "Content-Type: application/json" \
   -d "{\"quiz_category\":{\"id\":3, \"type\":\"geography\"}, \ 
	    \"previous_questions\":[1,2]}" \ 
  http://localhost:5000/api/quizzes
  ```

- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}
```
###### Delete a question

`GET '/api/questions/<question_id>'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample Request
- Response: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```



## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
