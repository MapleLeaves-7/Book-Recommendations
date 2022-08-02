import { BookCard } from '.';

export function BookCardResults({
  title,
  books,
  noResultsMessage,
  isSearchResultsPage,
}) {
  let bookCardClass = 'grid w-full gap-4 justify-items-center grid-cols-fit';
  return (
    <div className="flex flex-col items-center w-full">
      <h2 className={isSearchResultsPage ? 'pb-3' : 'pb-3 sm:self-start'}>
        {title}
      </h2>
      <div
        className={
          isSearchResultsPage
            ? bookCardClass
            : bookCardClass + ' sm:justify-items-start'
        }
      >
        {books.length > 0 ? (
          books.map(result => (
            <BookCard
              key={result.id}
              id={result.id}
              title={result.title}
              authors={result.authors}
              img={result.book_cover}
            />
          ))
        ) : (
          <div className="pt-3 font-arvo">{noResultsMessage}</div>
        )}
      </div>
    </div>
  );
}
