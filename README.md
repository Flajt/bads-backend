# Bads Backend Demo

Small demo backend which is part of the BADs project.
It uses Bloom filters to allow privacy friendly advertisment.

## Run it

1. Install `docker` & `docker-compose`
2. Run: `docker-compose up` if you like with `-d` argument
3. You can check if things work by checking `localhost:8000/hello` that should respond with `Hello World`
4. You are redy to run

## What is included?
- Mongodb (db)
- Backend (backend)
- Minio (S3) storage

## Running the demo
If you want to run the app and SDk demo it might be usefull to generate some random ads, so that something can be displayed.
To generate these ads run:
`python3 util/populate_ads.py`

If you are done use:
`python3 util/clean_db.py` to wipe everything.

## Tests

1. Activate the python3 enviroment by running `source venv/bin/activate`
2. Run `pytest`

> Note: This project will be continued in the future

## Structure

- `src/model`: Contains all the model files that represent data
- `src/services`: Contains most of the services that wrap the db or the minio clinet (I forgott to move the AdService from `src` there as well)
- `src/tests`: Some tests to validate the core features, doesn't cover everything
- `src/util`: Utility scripts e.g. to populate db or wipe it
- `venv`: Virtual enviroment
