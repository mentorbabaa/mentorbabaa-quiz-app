CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  option_a TEXT,
  option_b TEXT,
  option_c TEXT,
  option_d TEXT,
  correct_answer TEXT
);

CREATE TABLE IF NOT EXISTS answers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  question_id INTEGER,
  selected_answer TEXT,
  is_correct BOOLEAN,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(question_id) REFERENCES questions(id)
);

-- Dummy Data
INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer) VALUES
('What is the capital of France?', 'London', 'Berlin', 'Paris', 'Madrid', 'C'),
('Which language is used for web apps?', 'Python', 'JavaScript', 'C++', 'Java', 'B'),
('What does CPU stand for?', 'Central Process Unit', 'Central Processing Unit', 'Computer Personal Unit', 'Central Processor Utility', 'B'),
('Which company created the iPhone?', 'Google', 'Samsung', 'Apple', 'Microsoft', 'C'),
('What is 2 + 2?', '3', '4', '5', '22', 'B');