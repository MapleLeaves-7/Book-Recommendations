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
      let max_num_results = 3;
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
    let showAllClassName =
      'border-gray-300 border-b-[2px] border-l-[2px] border-r-[2px] cursor-pointer hover:bg-gray-200';
    let activeClass = ' bg-gray-200';
    if (isShow && searchedWord) {
      if (results.length > 0) {
        return (
          <ul className="absolute top-0 z-10 w-full pt-2 font-arvo bg-off-white">
            {results.map((result, index) => {
              let resultClassName = 'flex gap-5 hover:bg-gray-200';
              if (index === 0) {
                resultClassName += ' pt-8';
              }

              return (
                <li
                  key={result.id}
                  className="border-gray-300 border-b-[2px] border-l-[2px] border-r-[2px]"
                >
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
                      className="w-20 p-1 pr-0 h-28 min-w-20 min-h-28"
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
                <p className="p-1 pl-4">...show all results</p>
              </li>
            ) : (
              <></>
            )}
          </ul>
        );
      }
    }
  };

  const handleBlur = () => {
    // have small timeout so that suggested book does not disappear when user clicks on it
    // and user will be redirected to book page instead
    setTimeout(function () {
      setIsShow(false);
    }, 100);
  };

  let baseSearchFormClass = 'flex flex-col items-center w-full gap-4';

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
          onBlur={handleBlur}
          onKeyDown={onKeyDown}
          className="relative z-20 w-full px-3 py-1 rounded-lg font-arvo shadow-search focus-visible:shadow-none focus-visible:outline-green-primary focus-visible:outline focus-visible:outline-2"
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
