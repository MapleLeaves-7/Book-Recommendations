# Book-Recommendations

![architecture
diagram](https://github.com/MapleLeaves-7/Book-Recommendations/blob/main/docs/architecture.svg?raw=true)

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
