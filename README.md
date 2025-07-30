
# Mentorbaba Quiz App

## Setup Instructions

### Requirements
- Python 3.8+
- MySQL Server
- pip packages listed in `requirements.txt`

### Steps

1. Create the MySQL database and run the script in `schema.sql` to create tables.
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create db and tables
   ```bash
   python init-db.py
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Navigate to `http://localhost:5000` in your browser.

### Notes
- Use `questions_template.xlsx` to add questions to the database.
- Login using any email/password. (Passwords are stored in plain text for simplicity.)

