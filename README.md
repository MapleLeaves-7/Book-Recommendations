# Book-Recommendations

![architecture
diagram](https://github.com/MapleLeaves-7/Book-Recommendations/blob/main/docs/architecture.svg?raw=true)

# Deployment instructions

Requirements:

1. Docker
2. Python 3.9
3. PostgreSQL 13

## Starting the website

1. Start the docker containers for the website and services from the root directory.

```
docker-compose up
```

2. To shut down the website, run the following command under the root directory.

```
docker-compose down
```

## Intial Setup (on a new machine)

This step only needs to be done once on a new machine.

Save the books to local database.

```
psql -U <username> -d books -f postgres_backup.sql
```

Once all the docker containers have started and the servers (search, db and website-backend) are accepting connections, run the installation script.

```
source setup.sh
```

# Development instructions

## Requirements

1. [Python](https://www.python.org/downloads/) 3.9 and above
2. [Node.js](https://nodejs.org/en/download/) v16 and above
3. [Meilisearch](https://docs.meilisearch.com/learn/getting_started/quick_start.html#setup-and-installation)
4. [PostgreSQL](https://www.postgresql.org/download/) 13

### Download python packages

```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Download NPM packages

```
cd website/frontend
npm install
```

## Restoring SQL Data

Database sql dump is saved under `postgres_backup.sql` in root directory.

To restore books data into database:

```
psql -U <username> -d books < postgres_backup.sql
```

## Index data into search engine

Start the meilisearch server in root directory.

```
meilisearch --no-analytics
```

Run the script to index all the data.

```
python search/index_data.py --all
```

## Environment variables

A package like [autoenv](https://github.com/hyperupcall/autoenv) can be used to set environment variables.

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

## Running entire application locally

Running the application from root directory:

1. Start backend api

```
flask run
```

2. Start Meilisearch server

```
meilisearch --no-analytics
```

3. Start website

```
cd website/frontend
npm start
```

# Repository Structure and Contents

Repository is separate into 5 main parts.

1. Database
2. Scraper
3. Data Science
4. Search
5. Website

## 1. Database

The files relating to the database are under the `db` folder.

Files in this folder are used in all other parts (Scraper, Data Science, Search, Website) to connect to and communicate with database.

Files:

1. `db_config.py` gets the credentials to connect to the local PostgreSQL database.
2. `models.py` specifies the database schema using SQLAlchemy and is used by other files to communicate with the database.

Technologies used:

1. [PostgreSQL](https://www.postgresql.org/): Relational Database used to save the data
2. [SQLAlchemy](https://www.sqlalchemy.org/): Object Relational Mapper (ORM) used to create the database and tables, as well as save new entries

## 2. Scraper

The files relating to the web scraper are under the `books_scraper` folder.

This web scraper was built using the [Scrapy](https://docs.scrapy.org/en/latest/index.html) framework, and is used to scrape the [Goodreads](https://www.goodreads.com/) website.

The following metadata for each book is saved:

1. Link to goodreads page
2. Title
3. Authors
4. Description
5. Number of Pages
6. Number of Ratings
7. Date Published
8. Link to Book Cover
9. Language
10. Genres
11. Setting (place at which events in the book took place)
12. Related Books

This scraper has been run and has extracted the metadata of the books from the list ["Books That Everyone Should Read At Least Once"](https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?"). The related books for each book have been saved into the database, and the metadata for some of them have been crawled. Currently, if the script is run, it will get the book links from the database that have not been crawled, and will crawl them.

To run the books scraper (assuming you are in root directory):

```
cd books_scraper
scrapy crawl goodreads
```

To crawl other book lists on goodreads, modify the code in `spiders/goodreads.py` to the following.

```
def start_requests(self):
        # Replace links with links of Goodreads list(s) you want to crawl
        start_urls = ["https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?", "https://www.goodreads.com/list/show/147668.E_J_Koh_s_Books_to_Celebrate_Asian_American_Fiction_Non_Fiction_Memoir_Graphic_Novel_and_Poetry"]

        ## Comment out the following lines
        # start_urls = []
        # start_urls += self.get_db_links_recrawl_description()
        # start_urls += self.get_db_links_no_description()
        # start_urls += self.get_db_links()

        ## Crawl book list instead of individual book page
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)
            time.sleep(1)
            # yield scrapy.Request(url=url, callback=self.parse_book_metadata)
```

## 3. Data Science

The files relating to data science are in the `datascience` folder.

### Main script: `save_cosine_sim_matrix.py`

For each book, calculates the top 10 most similar books.

Techniques used:

1. Stemming
2. Stop word removal
3. TF-IDF Vectors
4. Cosine similarity

### Local testing: `output_local_cosine_sim.py`

Used to see how well the model predicts similar books. Similar books recommended by the current algorithm is compared with the related books extracted from Gooreads. Comparing related books extracted from Goodreads with the current book should yield a higher similarity score than comparing a random book with the current book. Results are dumped out into a json file in the `data` folder.

## 4. Search

The files relating to search are in the `search` folder.

Search functionality was implemented using [meilisearch](https://docs.meilisearch.com/). When the meilisearch server is running, the `index_data.py` script is used to index the data from database into the search engine.

### Main script: `index_data.py`

It takes the following command line options:

1. `-a` or `--all`: Indexes all the books in the database.
2. `-n NUM_BOOKS` or `--num_books NUM_BOOKS`: Specifies the number of books to index into search engine. This flag is ignored if `-a` flag is present
3. `-b BATCH_NUM` or `--batch_num BATCH_NUM`: Specifies the batch size to index the books with. Default is 500 books at a time.

Example usage:

```
# Indexes all the books into the search engine, 1000 books at a time.
python search/index_data.py --all -b 1000
```

### Local testing: `output_local.py`

Indexes the data with default arguments into the search engine and outputs the indexed data as a json file.

## 5. Website

The files relating to the website (frontend and backend) are in the `website` folder.

### Frontend

Languages used:

- Javascript
- HTML
- CSS

Technologies used:

- React
- Tailwind CSS

### Backend

Languages used:

- Python

Technologies used:

- Flask
- SQLAlchemy
