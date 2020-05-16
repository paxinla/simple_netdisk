# A simple file upload/download web service

This web service is for temporary file upload/download.

The files are stored in a directory. The relationship between the files and their download code are stored in a Sqlite file.

## Install

Under this directory, change the **secret key** in file privu/core.py , then run

```sh
$ python setup.py bdist_wheel
```

and a wheel package file will be appear in the path `dist/` 。Upload this `.whl` file to your VPS, then use pip to install it.


## Usage
### Configuration

A configuration file in json format is required. Example, a conf.json may looks like :

```json
{
 "host": "127.0.0.1",
 "port": 8000,
 "upload_location": "F:\\upfiles",
 "database_file_location": "F:\\app.db",
 "username": "admin",
 "userpassword": "231",
 "login_timeout": 3   // Time unit is minutes
}
```

### Run

```sh
$ privu --conf conf.json
```

