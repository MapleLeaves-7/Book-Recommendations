import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import searchService from '../services/search';
const { index } = searchService;

export function SearchBar() {
  const [results, setResults] = useState([]);
  const [searchedWord, setSearch] = useState('');
  const [hasMoreResults, setHasMoreResults] = useState(false);

  const navigate = useNavigate();
  const submitSearch = event => {
    event.preventDefault();

    navigate(`/search`, { state: searchedWord });
  };

  const handleSearchChange = ({ target }) => {
    setSearch(target.value);
    (async function () {
      let max_num_results = 5;
      const search = await index.search(target.value);
      if (search.hits.length > max_num_results) {
        setResults(search.hits.slice(0, max_num_results));
        setHasMoreResults(true);
      } else {
        setResults(search.hits);
        setHasMoreResults(false);
      }
    })();
  };

  const renderAutocomplete = () => {
    if (searchedWord) {
      if (results.length > 0) {
        return (
          <ul className="absolute w-full bg-off-white">
            {results.map(result => (
              <li key={result.id}>
                <Link to={`/book/${result.id}`} className="flex gap-5">
                  <img
                    src={result.book_cover}
                    alt={result.title}
                    className="w-24 h-36"
                  />
                  <span className="flex-wrap">{result.title}</span>
                </Link>
              </li>
            ))}
            {hasMoreResults ? (
              <li onClick={submitSearch} className="cursor-pointer">
                ...show all results
              </li>
            ) : (
              <></>
            )}
          </ul>
        );
      }
    }
  };

  return (
    <form
      onSubmit={submitSearch}
      className="flex flex-col items-center w-full gap-4"
    >
      <div className="relative w-10/12">
        <input
          name="Search"
          type="text"
          value={searchedWord}
          onChange={handleSearchChange}
          onFocus={handleSearchChange}
          className="w-full search-bar"
        />
        {renderAutocomplete()}
      </div>
      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
}
