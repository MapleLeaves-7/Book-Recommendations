import { SearchBar } from '../components';
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { BookCardResults } from '../components';

import searchService from '../services/search';
const { index } = searchService;

export function SearchResults() {
  const location = useLocation();
  const initialQuery = location.state ? location.state : '';
  const [searchResults, setResults] = useState([]);

  // load the search results when the page is first loaded
  useEffect(() => {
    // create and call scoped async function
    (async function () {
      const search = await index.search(initialQuery);
      setResults(search.hits);
    })();
  }, [initialQuery]);

  return (
    <div className="flex justify-center">
      {/* Container for all content in page */}
      <div className="flex flex-col items-center container-lg">
        {/* Section for Search Bar */}
        <SearchBar />

        {/* Section for Search Results */}
        <BookCardResults
          title={'Search results'}
          books={searchResults}
          noResultsMessage="Sorry, I could not find the book you were looking for."
          isSearchResultsPage={true}
        />
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
