import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app.secret_key = os.environ.get('SECRET_KEY')
        self.username = 'student'
        self.password = 'student'
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.username, self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_405_for_categories(self):
        res = self.client().post("/api/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


    def test_get_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))


    def test_404_request_beyond_valid_questions_page(self):
        res = self.client().get("/api/questions?page=500")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "page not found")


    def test_get_questions_search_with_results(self):
        res = self.client().post("/api/questions", json={"searchTerm": "lake"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 1) #change
        self.assertTrue(data["total_questions"])
        

    def test_get_book_search_without_results(self):
        res = self.client().post("/api/questions", json={"searchTerm": "zed za"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)


    def test_create_question(self):
        new_question = {
                    'question': 'What is the first alphabet?',
                    'answer': 'A',
                    'difficulty': '2',
                    'category': '2'
                }

        res = self.client().post("/api/questions", json=new_question)
        data = json.loads(res.data)

        saved_question = Question.query.filter_by(question=new_question['question']).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(new_question['answer'], saved_question.answer)


    def test_422_if_question_creation_fails(self):
        new_question = {
            'good question': 'What is the first alphabet?',
            'not answered': 'A'
         }
        res = self.client().post("/api/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable entity')


    def test_405_for_failed_create_question(self):
        res = self.client().patch("/api/questions", json={'question': 'will this request fail?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


    def test_delete_question(self):
        res = self.client().delete('/api/questions/6')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)


    def test_404_on_delete_question_does_not_exist(self):
        res = self.client().delete("/api/questions/10000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "question not found")


    def test_404_if_category_does_not_exist(self):
        res = self.client().get("/api/categories/99/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "category not found")

    
    def test_404_if_quiz_category_exist_or_does_not_have_questions(self):
        params = {
                    "previous_questions" : [],
                    "quiz_category" : {"id": 44, "type": ""}
                }

        res = self.client().post("/api/quizzes", json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "no questions or category does not exist")

    
    def test_422_quiz_invalid_previous_questions_type(self):
        params = {
                    "previous_questions" : "[]",
                    "quiz_category" : {"id": 2, "type": ""}
                }

        res = self.client().post("/api/quizzes", json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable entity")





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()