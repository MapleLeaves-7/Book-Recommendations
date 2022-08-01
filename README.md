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
python -m pip install -r search/requirements.txt
```

Run the script with the `--all` option.

```
python search/index_data.py -a
```

# Development instructions

Repository is separate into 5 main parts.

1. Database
2. Scraper
3. Datascience
4. Search
5. Website

## 1. Database

The files relating to the database are under the `db` folder.
A [PostgreSQ](https://www.postgresql.org/) database was used to save the data, and [SQLAlchemy](https://www.sqlalchemy.org/) was used to create the database and tables, as well as save new entries.

Files:

1. `db_config.py` gets the credentials to connect to the local PostgreSQL database.
2. `models.py` specifies the database schema using SQLAlchemy and is used by other files to communicate with the database.

## 4. Search

Search functionality was implemented using [meilisearch](https://docs.meilisearch.com/). When the meilisearch server is running, the `index_data.py` script is used to index the data from database into the search engine.

The `index_data.py` script takes the following command line options:

1. `-a` or `--all`: Indexes all the books in the database.
2. `-n NUM_BOOKS` or `--num_books NUM_BOOKS`: Specifies the number of books to index into search engine. This flag is ignored if `-a` flag is present
3. `-b BATCH_NUM` or `--batch_num BATCH_NUM`: Specifies the batch size to index the books with. Default is 500 books at a time.

Example usage:

```
# Indexes all the books into the search engine, 1000 books at a time.
python search/index_data.py --all -b 1000
```

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
