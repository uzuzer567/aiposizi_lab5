"""Module with routes for Flask application"""

import os
from datetime import datetime

from flask import (Blueprint, jsonify,
                   make_response,
                   request)

try:
    # Used for server setup using command line
    from spa_oauth.backend.modules.api.database_connection import connection, cursor
    from spa_oauth.backend.modules.api.status_codes import StatusCodes
    from spa_oauth.backend.modules.database.database_interactions import (close_connection,
                                                                          connect_to_database)
    from spa_oauth.backend.modules.database.document import Document
    from spa_oauth.backend.modules.database.user import User
    from spa_oauth.backend.modules.database.task import Task
    from spa_oauth.backend.modules.database.factory import Factory

    from spa_oauth.backend.modules.api.schemas import (AddNewUser, AddNewDocument,
                                                       AddNewTask, UpdateTableSchema,
                                                       AddNewFactory)
except ModuleNotFoundError as err:
    # Used for server setup using Docker
    from modules.api.database_connection import connection, cursor
    from modules.api.status_codes import StatusCodes
    from modules.database.database_interactions import close_connection, connect_to_database
    from modules.database.document import Document
    from modules.database.user import User
    from modules.database.task import Task
    from modules.database.factory import Factory

    from modules.api.schemas import (AddNewUser, AddNewDocument,
                                     AddNewTask, UpdateTableSchema,
                                     AddNewFactory)


get_blue_print = Blueprint('get_documentation', __name__, url_prefix=os.environ['API_PREFIX'])


@get_blue_print.route('/users')
def get_users():
    """View with users table"""

    user = User(connection=connection, cursor=cursor)

    all_users = user.get_all_users()

    context = {
        'all_users': all_users
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/documents')
def get_documents():
    """View with documents table"""

    document = Document(connection=connection, cursor=cursor)

    all_documents = document.get_all_documents()

    context = {
        'all_documents': all_documents
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/factories')
def get_factories():
    """View with factories table"""

    factory = Factory(connection=connection, cursor=cursor)

    all_factories = factory.get_all_factories()

    context = {
        'all_factories': all_factories
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/tasks')
def get_tasks():
    """View for showing new tasks"""

    task = Task(connection=connection, cursor=cursor)

    all_tasks = task.get_all_tasks()

    context = {
        'all_tasks': all_tasks
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/get_one_document/<int:idx>', methods=("GET", "POST"))
def get_one_document(idx: int):
    """View for one document page"""

    document = Document(connection=connection, cursor=cursor)
    document_description = document.get_document_by_id(document_id=idx)

    task = Task(connection=connection, cursor=cursor)
    all_document_tasks = task.get_task_by_document_id(document_id=idx)

    if isinstance(document_description['date_of_creation'], datetime):
        document_description['date_of_creation'] = str(document_description['date_of_creation'].date())

    if isinstance(document_description['date_of_registration'], datetime):
        document_description['date_of_registration'] = str(document_description['date_of_registration'].date())

    context = {
        'document_description': document_description,
        'all_document_tasks': all_document_tasks
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/get_one_factory/<int:idx>', methods=("GET", "POST"))
def get_one_factory(idx: int):
    """View for one factory page"""

    factory = Factory(connection=connection, cursor=cursor)
    factory_description = factory.get_factory_by_id(factory_id=idx)

    context = {
        'factory_description': factory_description,
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/get_one_task/<int:idx>', methods=("GET", "POST"))
def get_one_task(idx: int):
    """View for one task page"""

    task = Task(connection=connection, cursor=cursor)
    task_description = task.get_task_by_id(task_id=idx)

    context = {
        'task_description': task_description,
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/get_one_user/<int:idx>', methods=("GET", "POST"))
def get_one_user(idx: int):
    """View for one user page"""

    user = User(connection=connection, cursor=cursor)
    user_description = user.get_user_by_id(user_id=idx)

    context = {
        'user_description': user_description,
    }

    return make_response(jsonify(context), StatusCodes.OK)


@get_blue_print.route('/get_documents_by_date')
def get_documents_by_date():
    """View for table updating (using JQuery and ajax)"""

    update_table_schema = UpdateTableSchema()

    errors = update_table_schema.validate(request.args)

    # if user inputs not number or nothing, than show him all entries
    if errors:
        last_n_days = 0
    else:
        args = update_table_schema.dump(request.args)
        last_n_days = args['last_n_days']

    document = Document(connection=connection, cursor=cursor)

    if last_n_days == 0:
        documents_by_date = document.get_all_documents()
    else:
        documents_by_date = document.get_document_by_date(document_n_days=last_n_days)

    context = {
        'all_documents': documents_by_date
    }

    return make_response(jsonify(context), StatusCodes.OK)

