const API_BASE_URL = import.meta.env.MODE === 'production' 
  ? '/api/v1'  // Use relative URL in production
  : 'http://localhost:8000/api/v1';  // Use full URL in development

export const fetchChapters = async (book) => {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${encodeURIComponent(book)}/chapters`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching chapters for book ${book}:`, error);
    throw error;
  }
};

export const fetchVerses = async (book, chapterNumber) => {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${encodeURIComponent(book)}/chapters/${chapterNumber}/verses`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching verses for ${book} ${chapterNumber}:`, error);
    throw error;
  }
};

export const fetchThemes = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/themes`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching themes:', error);
    throw error;
  }
};

export const fetchBooks = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/books`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching books:', error);
    throw error;
  }
};

export const fetchThemeConnections = async (themeId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/themes/${themeId}/connections`);
    if (!response.ok) {
      if (response.status === 404) {
        return [];
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching connections for theme ${themeId}:`, error);
    throw error;
  }
};

export const fetchBookInsights = async (bookId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}/insights`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching insights for book ${bookId}:`, error);
    throw error;
  }
};
