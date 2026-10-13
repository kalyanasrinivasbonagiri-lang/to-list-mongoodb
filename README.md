# Flask & MongoDB Todo Application

A full-stack web application built with **Python**, **Flask**, and **MongoDB (PyMongo)**, designed for the B.Tech Lab Assignment: **“Web framework and a NoSQL database”** (Faculty of Engineering and Technology, JAIN Deemed-to-be University).

---

## 1. Project Overview

This project demonstrates how a lightweight Python web framework (**Flask**) interfaces with a document-oriented NoSQL database (**MongoDB**).

### Features
- **Task Viewing**: Retrieves all documents stored in MongoDB using `find()` and dynamically renders them on a clean, modern web interface.
- **Task Submission**: Accepts new tasks via an HTML form, sends a `POST` request to `/add`, and persists them into MongoDB using `insert_one()`.
- **Input Validation**: Prevents blank or whitespace-only task entries.
- **Resilient Connection Handling**: Automatically falls back between a local MongoDB instance and a cloud-hosted MongoDB Atlas cluster via the `MONGO_URI` environment variable.
- **Cloud-Ready**: Prepared with a `Procfile` and `requirements.txt` for deployment on Render.

---

## 2. Tech Stack & Architecture

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/) (Python micro-framework)
- **Database Driver**: [PyMongo](https://pymongo.readthedocs.io/) (Official Python driver for MongoDB)
- **Database**:
  - **Local Development**: Local MongoDB Server (`mongodb://localhost:27017/`)
  - **Cloud Production**: [MongoDB Atlas](https://www.mongodb.com/atlas) (Managed cloud database)
- **Frontend**: Semantic HTML5, Vanilla CSS, Jinja2 template engine
- **WSGI Production Server**: [Gunicorn](https://gunicorn.org/) (for Render cloud deployment)

---

## 3. End-to-End Request Flow

Understanding the flow of data helps you explain the architecture clearly to your evaluator:

```
[ Browser Client ]
       │
       │  1. HTTP GET /
       ▼
 [ Flask (app.py) ]
       │
       │  2. todos_collection.find()
       ▼
 [ MongoDB (beginner_db.todos) ]
       │
       │  3. Returns JSON-like BSON documents
       ▼
 [ Flask (Jinja2) ]
       │
       │  4. render_template("index.html", todos=all_todos)
       ▼
[ Browser Client ] ◄── 5. Renders interactive HTML page

─────────────────────────────────────────────────────────────

[ Browser Client ] (User fills form and clicks "Add Task")
       │
       │  1. HTTP POST /add  { task: "Complete assignment" }
       ▼
 [ Flask (app.py) ]
       │
       │  2. request.form.get("task") & validation
       │  3. todos_collection.insert_one({"task": task})
       ▼
 [ MongoDB (beginner_db.todos) ] (Document inserted)
       │
       │  4. Flask returns HTTP 302 Redirect to "/"
       ▼
[ Browser Client ] ── Re-fetches "/" and displays newly added task!
```

---

## 4. Project Structure

```
to-list-mongoodb/
├── app.py              # Main Flask application and database logic
├── requirements.txt    # Project dependencies for local & production
├── Procfile            # Deployment instruction for Render (WSGI entry point)
├── .gitignore          # Files excluded from Git tracking (.env, __pycache__)
├── .env.example        # Template for cloud environment variables
├── README.md           # Documentation and lab demonstration guide
├── templates/
│   └── index.html      # Jinja2 template for the web interface
└── static/
    └── css/
        └── style.css   # Custom responsive styling and design system
```

---

## 5. Local Setup & Execution (Windows PowerShell)

Follow these steps to run the application on your Windows machine.

### Step 5.1: Clone or Navigate to the Workspace
Open Windows PowerShell and navigate to your project directory:
```powershell
cd c:\Users\kalya\Desktop\to-list-mongoodb
```

### Step 5.2: Set Up Python Virtual Environment (Recommended)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Step 5.3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5.4: Ensure Local MongoDB is Running
On Windows, MongoDB runs as a background Windows Service. Check its status:
```powershell
Get-Service -Name MongoDB
```
If it is stopped, start it with administrator privileges:
```powershell
net start MongoDB
```

### Step 5.5: Run the Flask Application
```powershell
python app.py
```
Output will indicate:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 5.6: Open in Browser
Open your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 6. Verifying Data Using MongoDB Shell (`mongosh`)

You can directly inspect and verify documents saved by Flask using the official `mongosh` terminal.

Open a new PowerShell window and run:

### 1. Launch `mongosh`
```powershell
mongosh
```
> **Explanation**: Connects to the active local MongoDB daemon on port `27017`.

### 2. Switch to the Assignment Database
```javascript
use beginner_db
```
> **Explanation**: Switches the active database context to `beginner_db`. (If it does not exist yet, MongoDB creates it as soon as the first document is inserted).

### 3. Query All Todo Documents
```javascript
db.todos.find()
```
> **Explanation**: Retrieves all documents in the `todos` collection. You should see documents formatted like:
> ```json
> {
>   "_id": ObjectId("67..."),
>   "task": "Complete MongoDB assignment"
> }
> ```

### 4. Count the Documents
```javascript
db.todos.countDocuments()
```
> **Explanation**: Returns the exact integer count of documents currently stored inside `todos`.

---

## 7. Cloud Deployment: MongoDB Atlas & Render

### Part 1: MongoDB Atlas Configuration
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/) and sign in.
2. In your Project Overview, check your cluster:
   - If `Cluster0` is in **PAUSED** state, click the three dots (`...`) or cluster settings and click **Resume Cluster**.
3. **Configure Network Access**:
   - In the left sidebar, click **Network Access**.
   - Click **Add IP Address**.
   - Select **Allow Access from Anywhere** (`0.0.0.0/0`) so that Render's cloud servers can connect to your database.
4. **Configure Database Access (Credentials)**:
   - In the left sidebar, click **Database Access**.
   - Ensure a database user exists (e.g. `admin` or your chosen username) with **Read and write to any database** privileges.
   - Note down the username and password.
5. **Get Connection String**:
   - Go to **Database** -> **Clusters** -> click **Connect**.
   - Choose **Drivers** (Driver: Python).
   - Copy the URI string:
     ```
     mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```
   - Replace `<username>` and `<password>` with your database user credentials.

### Part 2: Deploy to Render
1. Push your project code to a GitHub repository:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit of Flask Todo App with MongoDB"
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```
2. Open [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** -> **Web Service**.
4. Select your connected GitHub repository.
5. Configure the service settings:
   - **Name**: `flask-mongodb-todo` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
6. Under **Environment Variables**:
   - Click **Add Environment Variable**.
   - **Key**: `MONGO_URI`
   - **Value**: Your MongoDB Atlas connection string from Part 1.
7. Click **Create Web Service**.
8. Once Render completes the build, your live application URL will appear at:
   `https://<your-service-name>.onrender.com`

---

## 8. Common Errors & Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `ServerSelectionTimeoutError: No replica set members match selector` | MongoDB service is stopped or wrong connection URI | Run `net start MongoDB` on Windows, or check Atlas IP Whitelist (`0.0.0.0/0`). |
| `bad auth: authentication failed` | Incorrect Atlas username or password | Recheck user credentials in Atlas -> Database Access. URL-encode special characters in password. |
| `gunicorn : The term 'gunicorn' is not recognized` on Windows | Gunicorn relies on UNIX system calls (fcntl/fork) | Run `python app.py` locally on Windows. Gunicorn is used in `Procfile` exclusively for Render (Linux). |
| Empty tasks appearing | Submitting form with only spaces | Handled in `app.py` with `task.strip()` and HTML `required` attribute. |

---

## 9. Faculty Demonstration Walkthrough

When presenting this lab assignment to your evaluator:

1. **State the Goal**:
   > *"This project implements a web application using the Flask micro-framework and a MongoDB NoSQL database to perform CRUD operations (Create and Read) following the lab requirements."*
2. **Explain the Architecture**:
   > *"The application uses Flask for routing (`/` and `/add`), PyMongo as the driver to interface with MongoDB, and Jinja2 for dynamic server-side rendering of documents from the `beginner_db` database and `todos` collection."*
3. **Demonstrate Task 1 (Local Execution)**:
   - Open PowerShell and show `python app.py`.
   - Open browser at `http://127.0.0.1:5000`.
   - Add a task: *"Complete MongoDB Assignment"*. Show it appearing immediately on the list.
   - Switch to PowerShell and run `mongosh`:
     ```javascript
     use beginner_db
     db.todos.find()
     ```
   - Show the document with `_id` and `task` fields matching the web UI.
4. **Demonstrate Task 2 (Cloud Readiness)**:
   - Show `Procfile` (`web: gunicorn app:app`) and `requirements.txt`.
   - Explain how `os.environ.get("MONGO_URI")` enables zero-code-change switching from localhost to MongoDB Atlas on Render.
