import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export function Main() {
  const [searchedWord, setSearch] = useState('');
  const navigate = useNavigate();
  const submitSearch = event => {
    event.preventDefault();

    navigate(`/search`, { state: searchedWord });
  };

  return (
    <div>
      <div className="flex flex-col items-center w-screen gap-3 py-4 font-arvo">
        <h1 className="text-xl font-bold ">Find books similar to...</h1>
        <form
          onSubmit={submitSearch}
          className="flex flex-col items-center w-full gap-4"
        >
          <input
            name="Search"
            type="text"
            value={searchedWord}
            onChange={({ target }) => setSearch(target.value)}
            className="w-10/12 px-3 py-1 border-transparent rounded-lg shadow-search"
          />
          <button
            type="submit"
            className="w-32 py-1 text-white rounded-md shadow-button bg-button"
          >
            Search
          </button>
        </form>
      </div>
    </div>
  );
}
