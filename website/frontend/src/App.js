import { Main, BookResult } from './pages';
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
          <Route path="/book/:id" element={<BookResult />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
