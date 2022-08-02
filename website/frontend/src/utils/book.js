const getAuthorDisplay = authors => {
  let authors_display = '';
  for (let author of authors) {
    authors_display += `${author.name}, `;
  }
  authors_display = authors_display.slice(0, authors_display.length - 2);
  return authors_display;
};

const getShortDescription = description => {
  let words = description.split(' ');
  if (words.length < 60) {
    return description;
  }

  return words.slice(0, 57).join(' ');
};

const bookUtils = { getAuthorDisplay, getShortDescription };

export default bookUtils;
