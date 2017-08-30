
## About
Django web application that parses, displays and filters data from a csv file.

## Installation

To run the project you'll need to install [Docker](https://docs.docker.com/compose/install/). 
With Docker installed, please run the following commands:

1. Build and start up the containers
```bash
$ docker-compose build 
```
```bash
$ docker-compose up 
```

2. Run the migrations
```bash
$ docker-compose run web ./manage.py migrate
```

3. Populate the database
```bash
$ docker-compose run web ./manage.py shell
>>> from reportsapp.tasks import report_processing
>>> report_processing.delay()
```

4. Point your browser to http://localhost:8000/

## Testing 

1. To run all the tests of the application
```bash
$ docker-compose run web ./manage.py test 
```

## Considerations

- The script to extract data from the csv was created as a task and scheduled to run at 4:30a.m.
- The database it's already ensuring that values to be saved in the Occurrence table should be always distinct - i.e. 'device' and 'timestamp' when together should be unique.
