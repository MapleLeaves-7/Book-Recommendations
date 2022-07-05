export function BookHits({ link, title, description, authors }) {
  return (
    <div>
      <h2>{title}</h2>
      <ul>
        {authors.map(author => (
          <li key={author.link}>{author.name}</li>
        ))}
      </ul>
      <p>Goodreads Link: {link}</p>
      <p>Description: {description}</p>
    </div>
  );
}
