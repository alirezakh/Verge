"""Verge (Client): App-Versions storage REST API.

This is the implementation of the client side to send requests to the server.

BY: ALIREZA KHATAMIAN
"""

from absl import app
from absl import flags
import base64
import json
import requests
from typing import Any, Sequence


FLAGS: flags.FLAGS = flags.FLAGS
flags.DEFINE_string('server', 'http://localhost', 'Server IP address.')
flags.DEFINE_integer('port', 8080, 'Server port number.')
flags.DEFINE_enum(
    'action', 'help', 
    ['help', 'create', 'get_all', 'get', 'upload', 'download'], 
    'Action to be made.')
flags.DEFINE_enum('type', 'app', ['app', 'version'], 'Sub action.')
flags.DEFINE_string('id', None, 'ID of an application to create/retrieve.')
flags.DEFINE_string('name', None, 'Name of an application to create.')
flags.DEFINE_string('version_id', None, 
                    'Version ID of an application to create/retrieve.')
flags.DEFINE_string('path', None, 
                    'Path to the file to upload or where to download.')


def help() -> None:
    """Sends GET request to the server root."""
    response = requests.get(f'{FLAGS.server}:{FLAGS.port}')
    print(response, response.text)


def create_application(id: str, name: str) -> None:
    """Creates a new application."""
    response = requests.post(
        f'{FLAGS.server}:{FLAGS.port}/apps', 
        data={
            'id': id,
            'name': name,
        })
    print(response, response.text)


def get_applications() -> None:
    """Returns all applications."""
    response = requests.get(f'{FLAGS.server}:{FLAGS.port}/apps')
    print(response, response.text)


def get_application(id: str) -> None:
    """Returns details for a specific application."""
    response = requests.get(f'{FLAGS.server}:{FLAGS.port}/apps/{id}')
    print(response, response.text)


def create_version(id: str, vid: str) -> None:
    """Creates a version for an application."""
    response = requests.post(f'{FLAGS.server}:{FLAGS.port}/apps/{id}/{vid}')
    print(response, response.text)


def get_version(id: str, vid: str) -> None:
    """Returns a version of an application."""
    response = requests.get(f'{FLAGS.server}:{FLAGS.port}/apps/{id}/{vid}')
    print(response, response.text)


def upload_file(id: str, vid: str, filename: str, path: str) -> None:
    """Uploads a file for an application and version.

    This method assumes that the file is not that large and
    can be uploaded without streaming.
    """
    files = {'file': (filename, open(path, 'rb'))}
    url = f'{FLAGS.server}:{FLAGS.port}/apps/{id}/{vid}/file'
    response = requests.post(url, files=files)
    print(response, response.text)


def download_file(filename: str, path: str) -> None:
    """Downloads a file identified by its name."""
    response = requests.get(f'{FLAGS.server}:{FLAGS.port}/files/{filename}')
    if response.ok:
        with open(path, 'wb') as f:
            f.write(base64.b64decode(response.text))
    print(response, response.text)


def main(args: Sequence[str]) -> None:
    """Redirects the requests based on the provided flags."""
    if FLAGS.action == 'help':
        help()
    elif FLAGS.action == 'create':
        if FLAGS.type == 'app':
            create_application(FLAGS.id, FLAGS.name)
        elif FLAGS.type == 'version':
            create_version(FLAGS.id, FLAGS.version_id)
    elif FLAGS.action == 'get_all':
        if FLAGS.type == 'app':
            get_applications()
    elif FLAGS.action == 'get':
        if FLAGS.type == 'app':
            if FLAGS.id:
                get_application(FLAGS.id)
        if FLAGS.type == 'version':
            if FLAGS.id and FLAGS.version_id:
                get_version(FLAGS.id, FLAGS.version_id)
    elif FLAGS.action == 'upload':
        if FLAGS.id and FLAGS.version_id and FLAGS.name and FLAGS.path:
            upload_file(FLAGS.id, FLAGS.version_id, FLAGS.name, FLAGS.path)
    elif FLAGS.action == 'download':
        if FLAGS.name and FLAGS.path:
            download_file(FLAGS.name, FLAGS.path)


if __name__ == '__main__':
    app.run(main)