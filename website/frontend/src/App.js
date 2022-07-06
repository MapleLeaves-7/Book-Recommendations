import { Main, BookResult } from './pages';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/book/:id" element={<BookResult />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
