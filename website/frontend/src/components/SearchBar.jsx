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
        className="w-10/12 px-3 py-1 border-transparent rounded-lg shadow-search focus-visible:outline-green-primary focus-visible:outline focus-within:outline-2"
      />
      <button
        type="submit"
        className="w-32 py-1 text-white rounded-md shadow-button bg-green-primary"
      >
        Search
      </button>
    </form>
  );
}
