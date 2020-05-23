import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''

# db_drop_and_create_all()


@app.route('/status/am-i-up', methods=['GET'])
def am_i_up():
    """Check to see if the app is running

    Returns:
        response, code -- the response and code
    """

    response = jsonify({
        "success": True,
    })

    return response, 200


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        - a public endpoint
        -contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    '''Get the drinks short decription.
        - a public endpoint
        -contain only the drink.short() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    Permissions:
        None

    '''
    response = jsonify({
        "drinks": [drink.short() for drink in Drink.query.all()],
        "success": True
    })

    return response, 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks_detailed():
    '''Get the drinks long decription.
        - a public endpoint
        -contain only the drink.short() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    Permissions:
        get:drinks-detail

    '''
    response = jsonify({
        "drinks": [drink.long() for drink in Drink.query.all()],
        "success": True
    })

    return response, 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found_error(error):
    response = jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    })
    return response, 404


@app.errorhandler(AuthError)
def unprocessible_entity_error(error):
    response = jsonify({
        "success": False,
        "error": error.status_code,
        "message": "AuthError: {}".format(error.error)
    })
    return response, error.status_code
