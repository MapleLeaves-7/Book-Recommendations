import axios from 'axios';
const baseUrl = 'http://127.0.0.1:5000/api/book';

const getBook = async id => {
  const response = await axios.get(`${baseUrl}/${id}`);
  return response.data;
};

const getSimilarBooks = async id => {
  const response = await axios.get(`${baseUrl}/similar_books/${id}`);
  return response.data;
};

const bookService = { getBook, getSimilarBooks };

export default bookService;
