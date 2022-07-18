import { Main, BookPage, SearchResults } from './pages';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <div>
      <Router>
        <nav>
          <Link to="/">SimilarBookSearch</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/book/:id" element={<BookPage />} />
          <Route path="/search" element={<Main />} />
          <Route path="/search/:query" element={<SearchResults />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
