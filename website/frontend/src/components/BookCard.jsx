export function BookCard({ id, link, title, description, authors }) {
  return (
    <a href={id}>
      <h2>{title}</h2>
      <ul>
        {authors.map(author => (
          <li key={author.link}>{author.name}</li>
        ))}
      </ul>
      <a href={link}>Goodreads Link: {link}</a>
      <p>Description: {description}</p>
    </a>
  );
}
