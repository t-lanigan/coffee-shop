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
# Login: https://tylers-test.auth0.com/authorize?audience=coffee&response_type=token&client_id=c2N45IwUfzUSG4mFLQAgotZ2aOP73xy9&redirect_uri=https://127.0.0.1:8080/login-results
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


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
@app.route('/drinks', methods=['GET'])
def get_drinks():
    '''Get the drinks short decription.
        - a public endpoint
        -contain only the drink.short() data representation
    Returns:
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    '''
    response = jsonify({
        "drinks": [drink.short() for drink in Drink.query.all()],
        "success": True
    })

    return response, 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detailed(request):
    """Get the drinks long decription.
        - a public endpoint
        - contain only the drink.short() data representation
    Returns:
        status_code int, response json -- {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    response = jsonify({
        "drinks": [drink.long() for drink in Drink.query.all()],
        "success": True
    })

    return response, 200


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drinks(payload):
    """Adds a new drink to the database.

    Arguments:
        payload json -- the recipe for the drink.

    Returns:
        status_code int, response json -- status code 200 and json {"success": True, "drinks": drink}
            where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    """

    try:
        body = request.get_json()
        recipe = body.get("recipe")
        title = body.get("title")

        if type(body.get("recipe")) is dict:
            recipe = json.dumps([recipe])

        else:
            recipe = json.dumps(recipe)

        drink = Drink(
            title=title,
            recipe=recipe
        )
        drink.insert()
        return jsonify({
            "success": True,
            "drink": drink.long()
        }), 201
    except:
        abort(422)


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drinks(*args, **kwargs):
    """Edits an existing drink

    Arguments:
        drink_id int -- the drink id to edit

    Returns:
        status_code int and response json -- {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    drink_id = kwargs.get("id")
    body = request.get_json()
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    if not drink:
        return jsonify({
            "success": True,
            "message": "Drink id: {} not found".format(drink_id)
        }), 404

    drink.recipe = body.get("recipe", drink.recipe)
    drink.title = body.get("title", drink.title)
    if isinstance(drink.recipe, list):
        drink.recipe = json.dumps(drink.recipe)
    drink.update()

    return jsonify({
        "success": True,
        "drink": drink.long()
    }), 200


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("patch:drinks")
def delete_drinks(*args, **kwargs):
    """Deletes drink id, where <id> is the existing model id

    Arguments:
        drink_id int -- The ID of the drink to be deleted.

    Returns:
        status_code int, response json -- status code 200 and {"success": True, "delete": id} where id is the id of the deleted record
    """
    drink_id = kwargs.get("id")
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    print(drink)
    if not drink:
        return jsonify({
            "success": False,
            "message": "No drink found for drink ID: {}".format(drink_id)
        }), 404
    drink.delete()
    return jsonify({
        "success": True,
        "delete": drink_id
    }), 200


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


@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({
        "success": False,
        "message": "There was an internal service error: {}".format(error)
    })
    return response, 500
