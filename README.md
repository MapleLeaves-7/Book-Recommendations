# Book-Recommendations

![architecture
diagram](https://github.com/MapleLeaves-7/Book-Recommendations/blob/main/docs/architecture.svg?raw=true)

# Deployment instructions

Docker must first be installed and running on the host machine.

To start the website, run the following command under the root directory.

```
docker-compose up
```

To shut down the website, run the following command under the root directory.

```
docker-compose down
```

On a brand new machine, the following steps must be done when the website is running. They only need to be done once.

1. Save the postgres SQL data into docker container

```
cat postgres_backup.sql | docker exec -i <name-of-docker-container-for-psql> psql -U user books
```

2. Index the meilisearch data into docker container

Create a new python virtual environment

```
python -m venv venv
source venv/bin/activate
```

Download the requirements

```
python -m pip install -r requirements.txt
```

Run the script with the `--all` option.

```
python search/index_data.py -a
```

# Development instructions

### Transferring SQL Data

When restoring books.dump into TablePlus database, set it as (--clean and --create)

### Requirements

meilisearch must be installed (https://docs.meilisearch.com/learn/getting_started/quick_start.html#setup-and-installation)

using homebrew

```
# Update brew and install Meilisearch
brew update && brew install meilisearch

# Launch Meilisearch
meilisearch
```

### Environment variables

```
HOSTNAME='localhost'
USERNAME=<yourdbusername>
PORT=<yourdbport>
PASSWORD=<yourdbpassword>
FLASK_APP="./website/backend/books_api"
```

Optional:

```
FLASK_ENV="development"
```

### Running the entire application

1. To run the backend api, enter `flask run` at root directory
2. To run meilisearch, enter `meilisearch --no-analytics ` at root directory
3. Enter `npm start` in website/frontend to start the whole application
