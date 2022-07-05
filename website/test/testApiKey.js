import { MeiliSearch } from 'meilisearch';

(async () => {
  const client = new MeiliSearch({
    host: 'http://127.0.0.1:7700',
    apiKey: process.env.MEILI_FRONTEND_API_KEY,
  });
  const books = await client.index('books').search('test');
  console.log(books);
})();

// client.index('books').search();
