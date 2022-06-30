import meilisearch
import json

client = meilisearch.Client('http://127.0.0.1:7700')

json_file = open('books.json')
books = json.load(json_file)
# client.index('books').delete_all_documents()
client.index('books').add_documents(books)