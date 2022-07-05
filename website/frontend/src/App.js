import { useEffect, useState } from 'react';
import { MeiliSearch } from 'meilisearch';
import { BookCard } from './components';

const client = new MeiliSearch({
  host: 'http://127.0.0.1:7700',
  // apiKey: process.env.MEILI_FRONTEND_API_KEY,
});

const index = client.index('books');

function App() {
  const [searchedWord, setSearch] = useState('');
  const [searchResults, setResults] = useState([]);

  useEffect(() => {
    // create and call scoped async function
    (async function () {
      const search = await index.search(searchedWord);
      setResults(search.hits);
    })();
  }, [searchedWord]);

  return (
    <div>
      <input
        name="Search"
        type="text"
        value={searchedWord}
        onChange={({ target }) => setSearch(target.value)}
      />
      <div>
        <h1>searched results</h1>
        {searchResults.map(result => (
          <BookCard
            key={result.id}
            link={result.link}
            title={result.title}
            description={result.description}
            authors={result.authors}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
