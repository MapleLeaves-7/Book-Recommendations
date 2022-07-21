import { BookCard } from '.';

export function BookCardResults({ title, books, noResultsMessage }) {
  return (
    <div className="w-full">
      <h2 className="pb-3">{title}</h2>
      <div className="grid gap-4 grid-cols-fit">
        {books.length > 1 ? (
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
