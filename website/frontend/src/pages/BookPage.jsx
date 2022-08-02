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
      <div className="flex justify-center">
        <div className="container-xl">
          {/* Section for all book metadata */}
          <div className="flex pt-2 pb-12 font-titillium">
            {currentBook.book_cover === 'None' ? (
              <div className="flex flex-col items-center flex-shrink-0 rounded-sm shadow-lg w-52 h-80">
                <p className="pb-8">(No Book Cover)</p>
                <p className="text-lg text-center">
                  Title: {currentBook.title}
                </p>
              </div>
            ) : (
              <img
                src={currentBook.book_cover}
                alt={currentBook.title}
                className="rounded-sm shadow-lg w-60 h-80"
              />
            )}
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
                {longDescription === shortDescription ? (
                  <></>
                ) : (
                  <span className="text-gray-500">
                    {showFullDescription ? '(' : '...('}
                    <span
                      onClick={() =>
                        setShowFullDescription(!showFullDescription)
                      }
                      className="link"
                    >
                      {showFullDescription ? 'less' : 'more'}
                    </span>
                    )
                  </span>
                )}
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
          <BookCardResults
            title={'Similar Books'}
            books={similarBooks}
            noResultsMessage="Sorry... I could not find any other similar books. Your book is unique!"
          />
        </div>
      </div>
    );
  }
}
