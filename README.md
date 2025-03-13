# Job Board

A full-stack job board application that crawls job postings from sites like Naukri.com and displays them in an interactive UI.

## Features

- Fetch job listings for a specific keyword (e.g., "Product Manager").
- Capture key attributes: Job Title, Company, Location, Experience, and Application Link.
- Build APIs to serve the crawled job data.
- Store job data in a database.
- Display job listings in a responsive UI with filters (e.g., location, experience).
- Include a search bar to query job titles.
- Pagination or infinite scrolling.
- Auto-refresh data every 24 hours.
- Job detail page with an apply button.
- Clean, minimalistic UI.

## Technologies Used

- **Backend**: Flask, SQLite, BeautifulSoup, undetected-chromedriver
- **Frontend**: React, Tailwind CSS, Framer Motion
- **Deployment**: (Specify your deployment platform, e.g., Heroku, Vercel, Netlify)

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend Setup

1. **Navigate to the Project Root Directory**:
   ```sh
   cd c:\Users\abhi3\OneDrive\Desktop\job-board
   ```

2. **Create the Virtual Environment Outside the `backend` Directory**:
   ```sh
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Navigate to the `backend` Directory**:
   ```sh
   cd backend
   ```

5. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

6. **Run the Flask Application**:
   ```sh
   python app.py
   ```

### Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```sh
   cd c:\Users\abhi3\OneDrive\Desktop\job-board\frontend
   ```

2. **Install Dependencies**:
   ```sh
   npm install
   ```

3. **Start the React Application**:
   ```sh
   npm start
   ```

### Running the Application

- **Backend**: Running on `http://127.0.0.1:5000`
- **Frontend**: Running on `http://localhost:3000`

### Testing

To run the tests, use the following command:

```sh
npm test
```

## Deployment

Specify the steps to deploy your application to your chosen platform.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspiration
- References
- etc.