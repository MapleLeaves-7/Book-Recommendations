import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BookCard } from '../components';

import searchService from '../services/search';
const { index } = searchService;

export function SearchResults() {
  const { query } = useParams;
  const [searchedWord, setSearch] = useState(query);
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
            id={result.id}
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
