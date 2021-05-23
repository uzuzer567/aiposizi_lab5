"""Module with interactions for task table"""

from typing import List, Dict


class Task:
    COLUMNS_TASK = [
        'id', 'task_name',
        'executor_id', 'document_id',
        'factory_id'
    ]

    def __init__(self, connection, cursor):
        """
        Class for faster interactions with user table

        :param connection: connection to database
        :param cursor: cursor for database
        """

        self.connection = connection
        self.cursor = cursor

    def add_task(self, task_name: str, executor_id: int,
                 document_id: int, factory_id: int):
        """
        Adds task to the database

        :param task_name: name of the task
        :param executor_id: id of the executor
        :param document_id: id of the document
        :param factory_id: id of the factory
        :return:
        """

        add_user_query = """
INSERT INTO task (task_name, executor_id, document_id, factory_id)
VALUES (%s, %s, %s, %s)
        """

        val = [task_name, executor_id, document_id, factory_id]

        self.cursor.execute(add_user_query, val)
        self.connection.commit()

    def get_all_tasks(self) -> List[Dict]:
        """
        Reads all task from database and returns it

        :return: list of all tasks
        """

        get_all_tasks_query = """
SELECT *
FROM task
        """

        self.cursor.execute(get_all_tasks_query)
        all_tasks = self.cursor.fetchall()

        all_tasks = [dict(zip(self.COLUMNS_TASK, curr_user)) for curr_user in all_tasks]

        return all_tasks

    def get_task_by_document_id(self, document_id) -> List[Dict]:
        """
        Reads task from database by document id and returns it.

        :param document_id: id of the document
        :return: list of tasks with given document id
        """

        get_all_tasks_query = """
SELECT *
FROM task
WHERE task.document_id = %s
        """

        val = [document_id]

        self.cursor.execute(get_all_tasks_query, val)
        all_tasks = self.cursor.fetchall()

        all_tasks = [dict(zip(self.COLUMNS_TASK, curr_user)) for curr_user in all_tasks]

        return all_tasks

    def get_task_by_id(self, task_id: int) -> Dict:
        """
        Finds task in database by its id and returns it.

        :param task_id: id of the task
        :return: task with given id
        """

        get_task_query = """
SELECT *
FROM task
WHERE task.id = %s
        """

        val = [task_id]

        self.cursor.execute(get_task_query, val)
        task = self.cursor.fetchall()[0]

        task = dict(zip(self.COLUMNS_TASK, task))

        return task

    def change_task(self, task_id: int, task_name: str, executor_id: int,
                    document_id: int, factory_id: int):
        """
        Adds task to the database

        :param task_id: index of the task
        :param task_name: name of the task
        :param executor_id: id of the executor
        :param document_id: id of the document
        :param factory_id: id of the factory
        :return:
        """

        change_task_query = """
UPDATE task
SET task_name = %s, executor_id = %s,
    document_id = %s, factory_id = %s
WHERE task.id = %s;
        """

        val = [task_name, executor_id, document_id, factory_id, task_id]

        self.cursor.execute(change_task_query, val)
        self.connection.commit()

    def delete_task(self, task_id: int):
        """
        Deletes task by id from database

        :param task_id: id of the factory
        """

        delete_task_query = """
DELETE FROM task
WHERE task.id = %s;
                """

        val = [task_id]

        self.cursor.execute(delete_task_query, val)
        self.connection.commit()



