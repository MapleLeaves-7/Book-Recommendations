import { useEffect, useState } from 'react';
import { BookCard, SearchBar } from '../components';

import bookService from '../services/books';

import { ReactComponent as RightArrowLogo } from '../images/right-arrow.svg';

export function Main() {
  const currentDisplayBookID = 196;
  const [currentBook, setCurrentBook] = useState(null);
  const [similarBooks, setSimilarBooks] = useState([]);
  useEffect(() => {
    (async function () {
      const currentBook = await bookService.getBook(currentDisplayBookID);
      const similarBooks = await bookService.getSimilarBooks(
        currentDisplayBookID
      );
      setCurrentBook(currentBook);
      setSimilarBooks(similarBooks.slice(0, 2)); // show only 2 similar books
    })();
  }, []);

  return (
    <div className="flex justify-center">
      <div className="flex flex-col items-center w-screen gap-3 font-arvo container-lg">
        <h1 className="text-xl font-bold ">Find books similar to...</h1>
        <SearchBar isMainPage={true} />

        {/* Section to show off similar books */}
        <div className="w-10/12 mt-6">
          <h2 className="pb-3">For example:</h2>
          <div className="box-border flex flex-col items-center justify-between px-10 pt-5 pb-8 rounded-md sm:flex-row sm:overflow-x-scroll bg-light-orange">
            {/* Section for current book */}
            <div>
              <h3 className="pb-2 text-lg">This book...</h3>
              {currentBook !== null && (
                <BookCard
                  id={currentBook.id}
                  title={currentBook.title}
                  authors={currentBook.authors}
                  img={currentBook.book_cover}
                />
              )}
            </div>

            <RightArrowLogo className="flex-shrink-0 w-20 py-3 rotate-90 sm:py-0 sm:px-2 opacity-70 sm:rotate-0" />
            {/* Section for similar books */}
            <div>
              <h3 className="pb-2 text-lg">...is similar to these</h3>
              <div className="flex flex-col justify-center gap-5 sm:flex-row">
                {similarBooks.length > 0
                  ? similarBooks.map(book => {
                      console.log(book);
                      return (
                        <BookCard
                          id={book.id}
                          title={book.title}
                          authors={book.authors}
                          img={book.book_cover}
                        />
                      );
                    })
                  : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
