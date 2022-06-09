
import os
from re import A
from unicodedata import category
from flask import Flask, request, abort, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories')
    def all_categories():
        categories = Category.query.all()
        formatted_categories = {category.format()['id']:category.format()['type'] for category in categories}
        session['current_category'] = 0
        return jsonify({
            'success': True,
            'categories': formatted_categories
        }), 200


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/questions', methods=['GET'])
    def all_questions():
        page = request.args.get('page', 1, type=int)
        start_index = (page - 1) * QUESTIONS_PER_PAGE
        end_index = start_index + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.all()
        formatted_categories = {category.format()['id']:category.format()['type'] for category in categories}
        session['current_category'] = 0
        
        return jsonify({
            'success': True,
            'questions': formatted_questions[start_index: end_index],
            'total_questions': len(formatted_questions),
            'current_category': 'active category',
            'categories': formatted_categories
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({
            'success': True
        }), 200

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/questions', methods=['POST'])
    def search_or_create_question():
        search_term = request.get_json().get('searchTerm', None)
        try:
            #question search
            if search_term:
                current_category = session.get('current_category', 0)
                if current_category != 0:
                    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).filter_by(category=current_category).all()
                else:
                    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

                formatted_questions = [question.format() for question in questions]

                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': current_category
                }), 200
            else:
            #question creation
                new_question = Question(**request.get_json())
                new_question.insert()
                return jsonify({
                    'success': True
                }), 200

        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/categories/<int:category_id>/questions')
    def category_questions(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        session['current_category'] = category_id
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': Category.query.get(category_id).type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/quizzes', methods=['POST'])
    def quiz():
        question = {}
        previous_questions_id = request.get_json().get('previous_questions', [])
        quiz_category = request.get_json().get('quiz_category', 0).get('id', 0)

        if quiz_category == 0:
            category_questions = Question.query.all() #handles 'all' category request
        else:
            category_questions = Question.query.filter_by(category=quiz_category).all()

        category_questions_id = [question.id for question in category_questions]
        next_question_id = random.choice(category_questions_id)

        if len(previous_questions_id) < len(category_questions):
            while next_question_id in previous_questions_id:
                next_question_id = random.choice(category_questions_id)
        else:
            next_question_id = None

        if next_question_id is not None:
            for q in category_questions: #avoids another interaction with db
                if q.id == next_question_id:
                    question = q.format()
                    break
            return jsonify({
                'success': True,
                'question': question
            }), 200
        else:
            return jsonify({
                'success': True,
            }), 200
            

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

