import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import searchService from '../services/search';
const { index } = searchService;

export function SearchBar({ isMainPage }) {
  const [active, setActive] = useState(null);
  const [results, setResults] = useState([]);
  const [searchedWord, setSearch] = useState('');
  const [hasMoreResults, setHasMoreResults] = useState(false);
  const [isShow, setIsShow] = useState(false);

  const navigate = useNavigate();

  const submitSearch = () => {
    setIsShow(false);
    navigate(`/search`, { state: searchedWord });
  };

  const handleEnter = event => {
    event.preventDefault();

    if (active >= 0 && active < results.length && active != null) {
      let bookID = results[active].id;
      return navigate(`/book/${bookID}`);
    }
    submitSearch();
  };

  const onKeyDown = e => {
    // up arrow
    if (e.keyCode === 38) {
      // if already at the first option, set to null
      if (active === 0) {
        return setActive(null);
      }
      // if at last "show more..." option, then set to last book results option
      if (active === -1) {
        return setActive(results.length - 1);
      }
      // otherwise set to previous book result option
      return setActive(active - 1);
    }

    // down arrow
    if (e.keyCode === 40) {
      if (active === null) {
        // go to the first option
        return setActive(0);
      }
      // at last book result option
      if (active + 1 === results.length) {
        // go to "show more..." option if it exists
        if (hasMoreResults) {
          return setActive(-1); // index -1 means that the "show more..." option is active
        }
        // at last book result option with no "show more..."
        return setActive(null);
      }
      // at the last "show more..."
      if (active === -1) {
        return setActive(null);
      }
      // go to the next option
      return setActive(active + 1);
    }
  };

  const handleSearchChange = ({ target }) => {
    setSearch(target.value);
    setIsShow(true);
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
    let showAllClassName = 'cursor-pointer';
    let activeClass = ' bg-gray-200';
    if (isShow && searchedWord) {
      if (results.length > 0) {
        return (
          <ul className="absolute w-full font-arvo bg-off-white">
            {results.map((result, index) => {
              let resultClassName = 'flex gap-5';
              return (
                <li key={result.id}>
                  <Link
                    to={`/book/${result.id}`}
                    className={
                      index === active
                        ? resultClassName + activeClass
                        : resultClassName
                    }
                  >
                    <img
                      src={result.book_cover}
                      alt={result.title}
                      className="w-24 h-40"
                    />
                    <span className="flex-wrap">{result.title}</span>
                  </Link>
                </li>
              );
            })}
            {hasMoreResults ? (
              <li
                onClick={submitSearch}
                className={
                  active === -1
                    ? showAllClassName + activeClass
                    : showAllClassName
                }
              >
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

  let baseSearchFormClass = 'flex flex-col items-center w-full gap-4';
  let baseSearchBarClass =
    'w-full font-arvo px-3 py-1 rounded-lg shadow-search focus-visible:outline-green-primary focus-visible:outline focus-visible:outline-2';

  return (
    <form
      onSubmit={handleEnter}
      className={
        isMainPage
          ? baseSearchFormClass
          : baseSearchFormClass + ' mb-8 md:flex-row'
      }
    >
      <div className="relative w-10/12">
        <input
          name="Search"
          type="text"
          value={searchedWord}
          onChange={handleSearchChange}
          onFocus={handleSearchChange}
          onBlur={() => {
            setIsShow(false);
          }}
          onKeyDown={onKeyDown}
          className={
            isMainPage ? baseSearchBarClass : baseSearchBarClass + 'md:w-10/12'
          }
        />
        {renderAutocomplete()}
      </div>
      <button
        type="submit"
        className="w-32 py-1 text-white rounded-md shadow-button bg-green-primary"
      >
        Search
      </button>
    </form>
  );
}
