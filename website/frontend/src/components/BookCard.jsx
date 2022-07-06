export function BookCard({ id, link, title, description, authors }) {
  return (
    <a href={`/book/${id}`}>
      <h2>{title}</h2>
      <ul>
        {authors.map(author => (
          <li key={author.link}>{author.name}</li>
        ))}
      </ul>
      <p>Description: {description}</p>
    </a>
  );
}
