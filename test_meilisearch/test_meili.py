import meilisearch
import json

client = meilisearch.Client('http://127.0.0.1:7700')

json_file = open('books/authors.json')
books = json.load(json_file)
client.index('books').add_documents(books)
# client.index('books').get_task(0)
 
# client.index('books').update_settings({
#   'filterableAttributes': [
#       'has_all_data',
#       'name'
#   ]
# })

# print(json.dumps(client.index('books').search('harper', {
#     'filter': 'has_all_data = True'
# }), indent=4))