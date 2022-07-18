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
      <form onSubmit={submitSearch}>
        <input
          name="Search"
          type="text"
          value={searchedWord}
          onChange={({ target }) => setSearch(target.value)}
        />
        <button type="submit">search</button>
      </form>
    </div>
  );
}
