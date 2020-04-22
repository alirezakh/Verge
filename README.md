Verge Backend: A simple web application, Verge, for storing and retrieving
different versions of software.

## Features ##
Verge allows a user to:
* Create a new Application (for example, "Google Chrome")
* Create a new Version (for example, "1.0.0")
* Upload Google-Chrome-1.0.0.exe and associate it with this Version
* View a list of Applications
* View a list of Versions for a given Application
(For simplicity, we won't have any user accounts.)

## Backend Specification ##
### Create Application ###
Creates an Application. 
`POST /apps`
```
Request:
    {
        "id": "google-chrome",
        "name": "Google Chrome"
    }
Response (200 OK):
    {
        "id": "google-chrome",
        "name": "Google Chrome"
    }
```

### Get All Applications ###
Gets all Applications.
`GET /apps` 
```
Returns:
    [
        {
            "id": "google-chrome",
            "name": "Google Chrome",
        },
        {
            "id": "adobe-photoshop-cc",
            "name": "Adobe Photoshop CC",
        },
        ...
    ]
```

### Get One Application ###
Gets the Application with the given tag, if one exists.
`GET /apps/<id>` 
Example: `GET /apps/google-chrome`
```
Returns:
    {
        "id": "google-chrome",
        "name": "Google Chrome",
        "versions": [
            { "id": "1.0", "file": "/files/Google-Chrome-1.0.0.exe" },
            { "id": "2.0", "file": null },
            { "id": "2.1", "file": null },
        ]
    }
```

### Create Version ###
Creates a Version for the Application with the given id.
`POST /apps/<id>/<version-id>`
Example: `POST /apps/google-chrome/1.0`

### Upload File for Version ###
Uploads the file (with multipart/form-data) to associate with this Version.
`POST /apps/<id>/<version-id>/file` 
Example: `POST /apps/google-chrome/1.0`

### Get One Version ###
Gets the Version for this Application with the given version-id, including the link to the file if it has been uploaded.
`GET /apps/<id>/<version-id>` 
Example: `GET /apps/google-chrome/1.0`
```
Returns:
    {
        "id": "1.0",
        "file": "/files/Google-Chrome-1.0.0.exe"
    }
```

### Download File ###
Download a version that has been uploaded with the Upload File for Version route.
`GET /files/<file>` 
Example: `GET /files/Google-Chrome-1.0.0.exe`