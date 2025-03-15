from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import logging
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DB_NAME = "jobs.db"

def init_db():
    """Initialize the database and create the jobs table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            company TEXT,
                            location TEXT,
                            experience TEXT,
                            link TEXT)''')
        conn.commit()

def save_to_db(jobs):
    """Save scraped jobs to the SQLite database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO jobs (title, company, location, experience, link) 
                              VALUES (?, ?, ?, ?, ?)''', jobs)
        conn.commit()

def get_jobs_from_db(search=None):
    """Fetch jobs from the database with an optional search filter."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        if search:
            logging.info(f"Searching for jobs with query: {search}")
            query = "SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ?"
            cursor.execute(query, (f"%{search}%", f"%{search}%"))
        else:
            cursor.execute("SELECT * FROM jobs")
        
        jobs = cursor.fetchall()
        
    return [{"id": job[0], "title": job[1], "company": job[2], "location": job[3], "experience": job[4], "link": job[5]} for job in jobs]

def scrape_jobs(keyword):
    """Scrape job listings from Naukri.com using Selenium and BeautifulSoup."""
    url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs"
    
    # Use Random User-Agent to Avoid Blocking
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = False  # Set to True after testing

    # Open Chrome browser
    driver = uc.Chrome(options=options)
    
    print("Scraping started...")
    
    try:
        driver.get(url)
        time.sleep(90)  # Increase wait time to ensure full load
        
        # Check if page loaded correctly
        if "captcha" in driver.page_source.lower():
            print("⚠️ Naukri is blocking the bot with CAPTCHA!")
            driver.quit()
            return []

        # Log the HTML content of the page
        print(driver.page_source)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        job_elements = soup.find_all("div", class_="jobTuple")  # ✅ Corrected Selector

        jobs = []
        for job in job_elements:
            title_tag = job.find("a", class_="title")
            company_tag = job.find("a", class_="subTitle")
            location_tag = job.find("li", class_="location")
            experience_tag = job.find("li", class_="experience")
            link = title_tag["href"] if title_tag else None

            jobs.append((
                title_tag.text.strip() if title_tag else "N/A",
                company_tag.text.strip() if company_tag else "N/A",
                location_tag.text.strip() if location_tag else "N/A",
                experience_tag.text.strip() if experience_tag else "N/A",
                link
            ))

        print(f"✅ Scraped {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"❌ Error while scraping: {str(e)}")
        return []
    finally:
        driver.quit()  # Ensure browser is closed properly

@app.route("/")
def home():
    """Render the home page with job listings."""
    search = request.args.get("search")
    jobs = get_jobs_from_db(search)
    return render_template("index.html", jobs=jobs, search=search)

@app.route("/scrape", methods=["GET"])
def scrape_and_store():
    """API to trigger job scraping and store results in DB."""
    keyword = request.args.get("keyword", "product manager")  # Default to "product manager" if no keyword is provided
    try:
        jobs = scrape_jobs(keyword)
        if jobs:
            save_to_db(jobs)
            return jsonify({"message": f"Scraped and stored {len(jobs)} jobs!", "jobs": jobs}), 200
        else:
            return jsonify({"error": "⚠️ No jobs found or scraping blocked! Try again later."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/jobs", methods=["GET"])
def get_jobs():
    """Retrieve job listings from the database and return them as JSON."""
    search = request.args.get("search")
    jobs = get_jobs_from_db(search)
    return jsonify(jobs), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)