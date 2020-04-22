# Verge: Client side application #

### Available APIs ###
To see all available APIs on the server side run the following command:
```python3 client/client.py --action help```

### Create a new application ###
```python3 client/client.py --action create --type app --id "google-chrome" --name "Google Chrome"```

### Create a new version ###
```python3 client/client.py --action create --type version --id "google-chrome" --version_id "1.0"```

### Retrieve an application ###
```python3 client/client.py --action get --type app --id "google-chrome"```

### Retrieve a version of an application ###
```python3 client/client.py --action get --type version --id "google-chrome" --version_id "1.0"```

### Retrieve all applications ###
```python3 client/client.py --action get_all --type app```

### Upload a file for a version of an applicatio ###
```python3 client/client.py --action download --name "<file_name>" --path "<path_to_file>"```

### Download a file from the server ###
```python3 client/client.py --action upload --id "google-chrome" --version_id "1.0" --name "<file_name>" --path "<path_where_to_save>"```

