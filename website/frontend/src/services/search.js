import { MeiliSearch } from 'meilisearch';

const client = new MeiliSearch({
  host: 'http://127.0.0.1:7700',
  // apiKey: process.env.MEILI_FRONTEND_API_KEY,
});

const index = client.index('books');

const searchService = { client, index };

export default searchService;
