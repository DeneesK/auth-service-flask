№ <b>User authorization service.

# Api Documentation

After starting the project, you will have access to the project documentation: [localhost:5000/apidocs]( http://localhost:5000/apidocs)

# Development

## Run auth app in dev mode

Copy `.env.sample` to `.env`. Execute `docker-compose up` to run in dev mode or `docker-compose up -f docker-compose.yml` to use production ready setup. The application will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


## Code style enforcement

Install [pre-commit](https://pypi.org/project/pre-commit/) python package to your environment (it is intentionally absent in requirements.txt) and run `pre-commit install` to install pre commit git hooks and check your code automatically before it's commited. It's handy to run `pre-commit` manually while working on code style issues or even use separate linting tools from `.pre-commit-config.yaml` eg. like *black* -  `black --skip-string-normalization` - to fix codestyle issues automatically.

## Running functional tests

Change your current directory to **tests/functional** then copy **.env.sample** to **.env** and execute `docker-compose up tests --no-log-prefix` to run tests.

## Naming conventions
Use **Data** postfix (eg. `UserData`) for marshmallow schema classes to use a feature of automatic sqlachemy objects serialization. It allows return sqlalchemy objects from flask view functions and also use them in **make_response** function.
