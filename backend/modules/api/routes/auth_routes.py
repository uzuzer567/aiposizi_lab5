"""Module with routes for app authentication"""

import os
import json
import urllib.parse

import requests
from flask import (
    Blueprint, Response,
    request, abort,
    make_response, jsonify,
    redirect
)
from oauthlib.oauth2 import WebApplicationClient


try:
    # Used for server setup using command line
    from spa_oauth.backend.modules.api.database_connection import connection, cursor
    from spa_oauth.backend.modules.api.status_codes import StatusCodes
    from spa_oauth.backend.modules.database.database_interactions import (close_connection,
                                                                          connect_to_database)
    from spa_oauth.backend.modules.database.app_user import AppUser
    from spa_oauth.backend.modules.database.factory import Factory

    from spa_oauth.backend.modules.api.schemas import AddNewAppUser, AddNewAppUserToken

    from spa_oauth.backend.modules.api.auth_utils import (
        get_google_provider_cfg,
        parse_user_info
    )
except ModuleNotFoundError as err:
    # Used for server setup using Docker
    from modules.api.database_connection import connection, cursor
    from modules.api.status_codes import StatusCodes
    from modules.database.database_interactions import close_connection, connect_to_database
    from modules.database.app_user import AppUser

    from modules.api.schemas import AddNewAppUser, AddNewAppUserToken

    from modules.api.auth_utils import (
        get_google_provider_cfg,
        parse_user_info
    )

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

auth_blue_print = Blueprint('auth_app', __name__, url_prefix=os.environ['API_PREFIX'])
web_app_client = WebApplicationClient(client_id=GOOGLE_CLIENT_ID)


@auth_blue_print.route('/auth/register', methods=("GET", "POST"))
def register_user():
    """View for user registration"""

    if request.method == 'POST':
        add_new_app_user_schema = AddNewAppUser()

        errors = add_new_app_user_schema.validate(data=request.form)

        if errors:
            abort(StatusCodes.BadRequest, str(errors))

        args = add_new_app_user_schema.dump(request.form)

        app_user = AppUser(connection=connection, cursor=cursor)

        user_with_given_email = app_user.get_app_user_by_email(email=args['email'])

        print('user_with_given_email', user_with_given_email)

        if user_with_given_email is None:
            new_user_id = app_user.add_app_user(
                email=args['email'],
                password=args['password']
            )

            auth_token = app_user.encode_auth_token(user_id=new_user_id)

            response_payload = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token
            }

            status_code = StatusCodes.Created
        else:
            response_payload = {
                'status': 'failed',
                'message': 'User with given email exists.',
            }
            status_code = StatusCodes.Forbidden

        return make_response(jsonify(response_payload), status_code)

    return Response(status=StatusCodes.BadRequest)


@auth_blue_print.route('/auth/login', methods=("GET", "POST"))
def login_user():
    """View for user registration"""

    if request.method == 'POST':
        add_new_app_user_schema = AddNewAppUser()

        errors = add_new_app_user_schema.validate(data=request.form)

        if errors:
            abort(StatusCodes.BadRequest, str(errors))

        args = add_new_app_user_schema.dump(request.form)

        app_user = AppUser(connection=connection, cursor=cursor)
        user_with_given_email = app_user.get_app_user_by_email(email=args['email'])

        if user_with_given_email:
            assert len(user_with_given_email) == 4, 'Bad number of columns'

            user_id = user_with_given_email['id']
            old_password_hash = user_with_given_email['password']

            auth_token = app_user.encode_auth_token(user_id=user_id)

            is_correct_password = app_user.check_correct_password(
                input_password=args['password'],
                old_password_hash=old_password_hash
            )

            if is_correct_password:
                response_payload = {
                    'status': 'success',
                    'message': 'Successful login.',
                    'auth_token': auth_token
                }

                status_code = StatusCodes.OK
            else:
                response_payload = {
                    'status': 'failed',
                    'message': 'Incorrect password.',
                }

                status_code = StatusCodes.Forbidden
        else:
            response_payload = {
                'status': 'failed',
                'message': 'No user with give email',
            }
            status_code = StatusCodes.NotFound

        return make_response(jsonify(response_payload), status_code)

    return Response(status=StatusCodes.BadRequest)


@auth_blue_print.route('/auth/loginGoogle', methods=("GET", "POST"))
def login_google():

    if request.method == 'POST':
        add_new_app_user_schema = AddNewAppUserToken()

        errors = add_new_app_user_schema.validate(data=request.form)

        if errors:
            abort(StatusCodes.BadRequest, str(errors))

        args = add_new_app_user_schema.dump(request.form)

        app_user = AppUser(connection=connection, cursor=cursor)
        user_with_given_email = app_user.get_app_user_by_email(email=args['email'])

        if user_with_given_email is None:
            new_user_id = app_user.add_app_user_token(
                email=args['email'],
                access_token=args['access_token']
            )

            response_payload = {
                'status': 'success',
                'message': 'Successfully created new user.',
                'auth_token': args['access_token']
            }

            status_code = StatusCodes.OK
        elif user_with_given_email['access_token'] == args['access_token']:
            response_payload = {
                'status': 'success',
                'message': 'Successful login',
                'auth_token': args['access_token']
            }

            status_code = StatusCodes.OK
        else:
            response_payload = {
                'status': 'failure',
                'message': 'Bad token',
            }

            status_code = StatusCodes.Forbidden

        return make_response(jsonify(response_payload), status_code)

    return Response(status=StatusCodes.BadRequest)
