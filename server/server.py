"""Verge (Server): App-Versions storage REST API.

This application is for storing and retrieving different versions of software.

BY: ALIREZA KHATAMIAN
"""

from absl import logging
import base64
import flask
import json
import os
import shutil
from typing import Any, Dict, List, Optional, Tuple, Union


app: flask.Flask = flask.Flask('Verge')
# To show available APIs when accessing the root
KEYS: Tuple[str, str, str] = ('Action', 'Pattern', 'Description')
APIs: Tuple[Tuple[str, str, str]] = (
    ('GET/POST', '/', 'Returns all available APIs.'),
    ('POST', '/apps', 'Creates a new Application.'),
    ('GET', '/apps', 'Returns all the stored applications.'),
    ('GET', '/apps/<id>', 'Returns an application with detailed information.'),
    ('POST', '/apps/<id>/<vid>', 'Creates a new version for an application.'),
    ('GET', '/apps/<id>/<version-id>', 
     'Returns a specific version of an application'),
    ('POST', '/apps/<id>/<version-id>/file', 
     'Uploads a file for an (application, version) pair.'),
    ('GET', '/files/<file>', 'Downloads requested file, if exists.'),
)
PATH = os.path.dirname(os.path.abspath(__file__))
STORAGE_NAME = 'files'
STORAGE_PATH = os.path.join(PATH, STORAGE_NAME)
# Dictionary-based databse that stores the applications and corresponding
# versions. This is a non-persistence database; i.e., data will vanish
# when the server gets shut down. A method will clean-up the residual files
# from previous run, when the server gets started again.
db: Dict[str, Dict[str, Union[str, Dict[str, Optional[str]]]]] = {}
# Dictionary that maps the file name to its path on the server.
# This mapping uses the filename provided by user as the key for fast 
# retrieval, therefore the filenames have to be unique among all applications
# and versions.
files: Dict[str, str] = {}
logging.set_verbosity(logging.INFO)


def cleanup() -> None:
    """Removes all the files stored on the server.
    
    This should be called before starting the server.
    """
    if os.path.exists(STORAGE_PATH):
        logging.info('Starting to clean up storage path: %s', STORAGE_PATH)
        shutil.rmtree(STORAGE_PATH)
    logging.info('Creating a new storage path: %s', STORAGE_PATH)
    os.mkdir(STORAGE_PATH)


@app.route('/', methods=['GET', 'POST'])
def get_available_apis() -> Tuple[Any, int]:
    """Returns available APIs when accessing root.
    
    Returns: Tuple of string response and HTTP code.
    """
    pattern = '{:<10}{:^30}{:>80}\n'
    response = pattern.format(*KEYS)
    for k in APIs:
        response += pattern.format(*k)
    return f'{response}\n', 200


def app_to_response(id: str) -> Optional[Dict[str, str]]:
    """Converts a specific application to proper response message.

    Returns: 
        A dictionary with id and name as keys and their corresponding values.
    """
    app = db.get(id, None)
    if not app:
        return None
    return dict(id=id, name=app.get('name', None))


def apps_to_response() -> List[Optional[Dict[str, str]]]:
    """Returns a list of all applications in db.

    Returns:
        List of dictionaries with id and name as keys
        and the corresponding values.
    """
    response = []
    for k, v in db.items():
        response.append(dict(id=k, name=v.get('name', None)))
    return response


def app_to_response_with_details(id: str) -> Optional[
    Dict[str, Union[str, List[Dict[str, Optional[str]]]]]]:
    """Converts a specific application to proper response message.

    Returns: 
        A dictionary with id and name as keys and their corresponding values.
    """
    app = db.get(id, None)
    if not app:
        return None
    response = dict(id=id, name=app.get('name', None), versions=[])
    versions = app.get('versions', None)
    if not versions:
        return response
    vers = []
    for k, v in versions.items():
        vers.append(dict(id=k, file=v))
    response.update(dict(versions=vers))
    return response


def version_to_response(id: str, vid: str) -> Optional[Dict[str, str]]:
    """Converts a specific version of an application to response message.

    Returns: 
        A dictionary with id and file as keys and their corresponding values.
    """
    app = db.get(id, None)
    if not app:
        return None
    versions = app.get('versions', None)
    if not versions or vid not in versions:
        return None
    return dict(id=vid, file=versions.get(vid, None))


@app.route('/apps', methods=['POST'])
def create_application() -> Tuple[Any, int]:
    """Creates a new application and stores it in db.

    Returns: Tuple of string response and HTTP code.
    """
    id = flask.request.form.get('id', default=None)
    name = flask.request.form.get('name', default=None)
    if not id or not name:
        logging.info('ID and name are required to create an application.')
        return 'ID and name are required to create an application.', 400
    if id in db:
        logging.info('Application (%s) already exists.', id)
        return f'Application ({id}) already exists.', 400
    db[id] = dict(name=name)
    logging.info('Application (%s: %s) is created.', id, name)
    return app_to_response(id), 200


@app.route('/apps', methods=['GET'])
def get_applications() -> Tuple[Any, int]:
    """Returns all the applications in the storage."""
    return json.dumps(apps_to_response()), 200


@app.route('/apps/<string:id>', methods=['GET'])
def get_application(id: str) -> Tuple[Any, int]:
    """Returns the specific application with details."""
    response = app_to_response_with_details(id)
    if not response:
        return f'Application ({id}) not found!', 404
    return json.dumps(response), 200


@app.route('/apps/<string:id>/<string:vid>', methods=['POST'])
def create_version(id: str, vid: str) -> Tuple[Any, int]:
    """Creates a new version for an application.

    Returns: Tuple of string response and HTTP code.
    """
    app = db.get(id, None)
    if not app:
        logging.info('Application (%s) not found!', id)
        return f'Application ({id}) not found!', 404
    versions = app.get('versions', None)
    if versions and vid in versions:
        logging.info('Version (%s) already exists for application (%s).', 
                        vid, id)
        return f'Version ({vid}) already exists for application ({id})', 400
    if not versions:
        app.update(dict(versions={vid: None}))
        logging.info(db)
        return f'Version ({vid}) is created for application ({id}).', 200
    app['versions'].update({vid: None})
    return f'Version ({vid}) is created for application ({id}).', 200


@app.route('/apps/<string:id>/<string:vid>', methods=['GET'])
def get_version(id: str, vid: str) -> Tuple[Any, int]:
    """Returns the specific version of an application."""
    response = version_to_response(id, vid)
    if not response:
        return f'Pair of application-version ({id}:{vid}) not found!', 404
    return json.dumps(response), 200


@app.route('/apps/<string:id>/<string:vid>/file', methods=['POST'])
def store_file(id: str, vid: str) -> Tuple[Any, int]:
    """Stores a file uploaded by user for a pair of application and versions.

    This method assumes that the file name is provided by the user.

    Returns: Tuple of string response and HTTP code.
    """
    app = db.get(id, None)
    if not app:
        logging.info('Application (%s) not found!', id)
        return f'Application ({id}) not found!', 404
    versions = app.get('versions', None)
    if not versions or vid not in versions:
        logging.info('Version (%s) for application (%s) not found!', id, vid)
        return f'Version ({vid}) for application ({id}) not found!', 404
    file = flask.request.files['file']
    filename = file.filename
    if filename in files:
        logging.info('%s already exists in the storage.', filename)
        return f'{filename} already exists in the storage.', 400
    storage_path = os.path.join(STORAGE_PATH, filename)
    with open(storage_path, 'wb') as f:
        f.write(file.read())
        db[id]['versions'][vid] = os.path.join(STORAGE_NAME, filename)
        files[filename] = storage_path
    return f'{filename} has been uploaded.', 200


@app.route('/files/<string:file>', methods=['GET'])
def retrieve_file(file: str) -> Tuple[Any, str]:
    """Retrieves a file from the storage.

    Returns: Tuple of string response and HTTP code.
    """
    if file not in files:
        logging.info('File (%s) not found!', file)
        return f'File ({file}) not Found!', 404
    with open(files.get(file), 'rb') as f:
        return base64.b64encode(f.read()), 200


if __name__ == '__main__':
    cleanup()  # Cleaning up the old files 
    app.run(host='127.0.0.1', port=8080, debug=True)
