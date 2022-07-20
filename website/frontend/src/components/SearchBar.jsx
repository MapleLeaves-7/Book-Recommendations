import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function SearchBar() {
  const [searchedWord, setSearch] = useState('');
  const navigate = useNavigate();
  const submitSearch = event => {
    event.preventDefault();

    navigate(`/search`, { state: searchedWord });
  };

  return (
    <form
      onSubmit={submitSearch}
      className="flex flex-col items-center w-full gap-4"
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
  );
}
