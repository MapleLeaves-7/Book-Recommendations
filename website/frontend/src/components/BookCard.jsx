import bookUtils from '../utils/book';

export function BookCard({ id, title, authors, img }) {
  if (title.length >= 29) {
    title = title.slice(0, 29) + '...';
  }

  let authors_display = bookUtils.getAuthorDisplay(authors);
  if (title.length + authors_display.length > 52) {
    authors_display = authors_display.slice(0, 21) + '...';
  }

  return (
    <div className="flex flex-col justify-center px-2 py-2 rounded-md bg-off-white w-52 h-80 shadow-sub-card font-titillium ">
      <a
        href={`/book/${id}`}
        className="flex flex-col items-center text-center"
      >
        <img src={img} alt={title} className="w-[150px] h-56 rounded-md" />
        <h3 className="mt-1 text-xl font-bold">{title}</h3>
        <p>
          by <span className="italic">{authors_display}</span>
        </p>
      </a>
    </div>
  );
}