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

# Repository Structure and Contents

Repository is separate into 5 main parts.

1. Database
2. Scraper
3. Datascience
4. Search
5. Website

## 1. Database

The files relating to the database are under the `db` folder.

Files in this folder are used in all other parts (Scraper, Data Science, Search, Website) to connect to and communicate with database.

Files:

1. `db_config.py` gets the credentials to connect to the local PostgreSQL database.
2. `models.py` specifies the database schema using SQLAlchemy and is used by other files to communicate with the database.

Technologies used:

1. [PostgreSQ](https://www.postgresql.org/): Relational Database used to save the data
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

## 3. Datascience

The files relating to data science are in the `datascience` folder.

Main script: `save_cosine_sim_matrix.py`

For each book, calculates the top 10 most similar books.

Techniques used:

1. Stemming
2. Stop word removal
3. TF-IDF Vectors
4. Cosine similarity

Local testing: `output_local_cosine_sim.py`

Used to see how well the model predicts similar books. Similar books recommended by the current algorithm is compared with the related books extracted from Gooreads. Comparing related books extracted from Goodreads with the current book should yield a higher similarity score than comparing a random book with the current book. Results are dumped out into a json file in the `data` folder.

## 4. Search

The files relating to search are in the `search` folder.

Search functionality was implemented using [meilisearch](https://docs.meilisearch.com/). When the meilisearch server is running, the `index_data.py` script is used to index the data from database into the search engine.

Main script: `index_data.py`. It takes the following command line options:

1. `-a` or `--all`: Indexes all the books in the database.
2. `-n NUM_BOOKS` or `--num_books NUM_BOOKS`: Specifies the number of books to index into search engine. This flag is ignored if `-a` flag is present
3. `-b BATCH_NUM` or `--batch_num BATCH_NUM`: Specifies the batch size to index the books with. Default is 500 books at a time.

Example usage:

```
# Indexes all the books into the search engine, 1000 books at a time.
python search/index_data.py --all -b 1000
```

`output_local.py` indexes the data with default arguments into the search engine and outputs the indexed data as a json file.

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
