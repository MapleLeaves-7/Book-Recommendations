import { Main, BookPage, SearchResults } from './pages';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <div>
      <Router>
        <nav className="py-4 text-white font-arvo bg-banner">
          <Link className="pl-6 text-xl" to="/">
            SIMILARSearch
          </Link>
        </nav>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/book/:id" element={<BookPage />} />
          <Route path="/search" element={<SearchResults />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
