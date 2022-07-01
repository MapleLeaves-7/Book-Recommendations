import json
from index_data import index_data

indexed_books = index_data()
with open('indexed_books.json', 'w') as f:
    json.dump(indexed_books, f, indent=4)