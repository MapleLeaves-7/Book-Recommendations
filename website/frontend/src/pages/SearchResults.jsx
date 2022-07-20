import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { BookCard } from '../components';

import searchService from '../services/search';
const { index } = searchService;

export function SearchResults() {
  const location = useLocation();
  const initialQuery = location.state ? location.state : '';
  const [searchedWord, setSearch] = useState(initialQuery);
  const [searchResults, setResults] = useState([]);

  // load the search results when the page is first loaded
  useEffect(() => {
    // create and call scoped async function
    (async function () {
      const search = await index.search(initialQuery);
      setResults(search.hits);
    })();
  }, [initialQuery]);

  // load the search results when the search is submitted
  const submitSearch = event => {
    event.preventDefault();
    (async function () {
      const search = await index.search(searchedWord);
      setResults(search.hits);
    })();
  };

  return (
    <div className="flex justify-center">
      <div className="flex flex-col items-center w-10/12 max-w-5xl ">
        <form
          onSubmit={submitSearch}
          className="flex items-center w-full gap-4 mt-8 mb-8"
        >
          <input
            name="Search"
            type="text"
            value={searchedWord}
            onChange={({ target }) => setSearch(target.value)}
            className="w-10/12 search-bar"
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </form>

        <div className="w-full">
          <h2>Search results</h2>
          <div className="grid grid-cols-fit">
            {searchResults.map(result => (
              <BookCard
                key={result.id}
                id={result.id}
                title={result.title}
                authors={result.authors}
                img={result.book_cover}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

//   useEffect(() => {
//     // create and call scoped async function
//     (async function () {
//       const search = await index.search(searchedWord);
//       setResults(search.hits);
//     })();
//   }, [searchedWord]);
