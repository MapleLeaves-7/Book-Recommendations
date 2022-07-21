import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BookCardResults } from '../components';
import bookService from '../services/books';
import bookUtils from '../utils/book';

export function BookPage() {
  const { id } = useParams(); // get bookID from url parameter
  const [currentBook, setCurrentBook] = useState(null);
  const [similarBooks, setSimilarBooks] = useState(null);
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [longDescription, setLongDescription] = useState('');
  const [shortDescription, setShortDescription] = useState('');

  useEffect(() => {
    const setBookData = async id => {
      const newCurrBook = await bookService.getBook(id);
      const newSimilarBooks = await bookService.getSimilarBooks(id);
      setCurrentBook(newCurrBook);
      setSimilarBooks(newSimilarBooks);
      setLongDescription(newCurrBook.description);
      setShortDescription(
        bookUtils.getShortDescription(newCurrBook.description)
      );
    };
    setBookData(id);
  }, [id]);

  if (currentBook) {
    return (
      <div className="flex justify-center pt-8">
        <div className="container-xl">
          {/* Section for all book metadata */}
          <div className="flex pb-12 font-titillium">
            <img
              src={currentBook.book_cover}
              alt={currentBook.title}
              className="w-60 h-80"
            />
            {/* Section for book text metadata */}
            <div className="pl-10">
              <h1 className="text-3xl font-bold">{currentBook.title}</h1>
              <p className="mb-3 text-lg">
                by{' '}
                <span className="italic">
                  {bookUtils.getAuthorDisplay(currentBook.authors)}
                </span>
              </p>
              <p className="text-[1.0625rem] pb-2">
                {showFullDescription ? longDescription : shortDescription}{' '}
                <spa className="text-gray-500">
                  (
                  <span
                    onClick={() => setShowFullDescription(!showFullDescription)}
                    className="link"
                  >
                    {showFullDescription ? 'less' : 'more'}
                  </span>
                  )
                </spa>
              </p>
              <p>
                Reference:{' '}
                <a href={currentBook.link} className="link">
                  {currentBook.link}
                </a>
              </p>
            </div>
          </div>

          {/* Section for Similar Books */}
          <BookCardResults title={'Similar Books'} books={similarBooks} />
        </div>
      </div>
    );
  }
}
