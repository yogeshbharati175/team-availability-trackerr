# TeamLite — Team Availability Tracker

A beginner-friendly, responsive team dashboard built with **Python, Flask, SQLite, HTML, and CSS**. It lets you track who is Available, Busy, or Away without needing a MySQL server.

## Preview

The dashboard includes summary cards, a searchable/filterable team table, status editing, and a form to add members.

## Features

- Dashboard counts for total, Available, Busy, and Away team members
- Add team members with a role and initial status
- Change a member's status
- Delete team members
- Search by name or role
- Filter by status
- Responsive layout for desktop and mobile
- SQLite database created automatically on first run
- Health-check endpoint at `/health`

## Tech stack

- Python 3.10+
- Flask
- SQLite
- HTML5 and CSS3

## Project structure

```text
team-lite-github-project/
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

The `team.db` file is created locally when you run the app. It is intentionally excluded from GitHub so each person gets their own database.

## Run locally on Windows

### 1. Install Python

Install Python 3.10 or newer. During installation, enable **Add Python to PATH**.

### 2. Open the project folder

Extract the ZIP. Open Command Prompt in the extracted `team_lite_github_project` folder.

### 3. Create a virtual environment

```bat
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```bat
python -m pip install -r requirements.txt
```

### 5. Start the application

```bat
python app.py
```

### 6. Open the dashboard

Visit <http://127.0.0.1:5000>.

No MySQL setup is needed. The app creates `team.db` and inserts sample members automatically on first run.

## GitHub upload instructions

1. Sign in to GitHub and create a repository named `team-lite`.
2. Extract this ZIP on your computer.
3. Open the extracted folder. Upload the **contents** of the folder to the repository, including `app.py`, `requirements.txt`, `.gitignore`, `.env.example`, `LICENSE`, `README.md`, `templates/`, and `static/`.
4. Do **not** upload `venv/`, `team.db`, or any passwords/secrets.
5. Commit the files to the `main` branch.

### Upload using Git (optional)

Run these commands in the project folder after creating an empty GitHub repository. Replace `YOUR-USERNAME` with your GitHub username.

```bat
git init
git add .
git commit -m "Initial commit: TeamLite availability tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/team-lite.git
git push -u origin main
```

If Git asks you to sign in, complete the GitHub authentication prompt.

## Deployment note

This project is intended as a learning/demo project. Before deploying publicly, configure a secure secret key, turn off Flask debug mode, and use a hosting service with persistent storage for SQLite. For multi-user production deployments, add authentication and authorization.

## License

Released under the MIT License. See `LICENSE`.
