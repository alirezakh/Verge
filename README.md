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
### Create Application POST /apps ###
Creates an Application.
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

### Get All Applications GET /apps ###
Gets all Applications.
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

### Get One Application GET /apps/<id> ###
Example: GET /apps/google-chrome
Gets the Application with the given tag, if one exists.
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

### Create Version POST /apps/<id>/<version-id> ###
Example: POST /apps/google-chrome/1.0
Creates a Version for the Application with the given id.

### Upload File for Version POST /apps/<id>/<version-id>/file ###
Example: POST /apps/google-chrome/1.0
Uploads the file (with multipart/form-data) to associate with this Version.

### Get One Version GET /apps/<id>/<version-id> ###
Example: GET /apps/google-chrome/1.0
Gets the Version for this Application with the given version-id, including the link to the file if it has been uploaded.
```
Returns:
    {
        "id": "1.0",
        "file": "/files/Google-Chrome-1.0.0.exe"
    }
```

### Download File GET /files/<file> ###
Example: GET /files/Google-Chrome-1.0.0.exe
Download a version that has been uploaded with the Upload File for Version route.