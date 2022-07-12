import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BookCard } from '../components';
import bookService from '../services/books';

export function BookPage() {
  const { id } = useParams(); // get bookID from url parameter
  const [currentBook, setCurrentBook] = useState(null);
  const [similarBooks, setSimilarBooks] = useState(null);

  useEffect(() => {
    const setBookData = async id => {
      const newCurrBook = await bookService.getBook(id);
      const newSimilarBooks = await bookService.getSimilarBooks(id);
      setCurrentBook(newCurrBook);
      setSimilarBooks(newSimilarBooks);
    };
    setBookData(id);
  }, [id]);

  if (currentBook) {
    return (
      <div>
        <h1>{currentBook.title}</h1>
        <ul>
          {currentBook.authors.map(author => (
            <li key={author.link}>{author.name}</li>
          ))}
        </ul>
        <a href={currentBook.link}>Goodreads Link: {currentBook.link}</a>
        <p>Description: {currentBook.description}</p>
        <h2>Similar Books</h2>
        {similarBooks.length > 0 &&
          similarBooks.map(result => (
            <BookCard
              key={result.id}
              id={result.id}
              link={result.link}
              title={result.title}
              description={result.description}
              authors={result.authors}
            />
          ))}
      </div>
    );
  }
}
