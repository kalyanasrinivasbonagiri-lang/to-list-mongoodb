import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

app = Flask(__name__)

# Retrieve connection string from environment variables, fallback to local for testing
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")

# Initialize MongoDB Client with a 3-second server selection timeout for responsive feedback
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client["beginner_db"]
todos_collection = db["todos"]


def check_db_connection():
    """Verify MongoDB connectivity via ping."""
    try:
        client.admin.command("ping")
        return True, None
    except (ConnectionFailure, ServerSelectionTimeoutError) as err:
        return False, f"Database connection error: {err}"
    except Exception as err:
        return False, f"Unexpected error connecting to MongoDB: {err}"


@app.route("/")
def index():
    """
    Home page route.
    Fetches all documents from the 'todos' NoSQL collection
    and renders them in index.html.
    """
    is_connected, error_msg = check_db_connection()
    all_todos = []

    if is_connected:
        try:
            # Fetch all documents from the NoSQL collection
            all_todos = list(todos_collection.find())
        except Exception as e:
            error_msg = f"Failed to fetch todos: {e}"
    
    return render_template(
        "index.html",
        todos=all_todos,
        db_connected=is_connected,
        db_error=error_msg,
        mongo_uri_source="MongoDB Atlas (Cloud)" if "mongodb.net" in MONGO_URI else "Localhost (mongodb://localhost:27017/)"
    )


@app.route("/add", methods=["POST"])
def add_todo():
    """
    Task creation route.
    Extracts the 'task' text from the submitted form,
    validates it, inserts a document into MongoDB, and redirects to home.
    """
    task = request.form.get("task")

    # Validate that task is not empty or just whitespace
    if task and task.strip():
        try:
            # Insert a JSON-like document into MongoDB
            todos_collection.insert_one({"task": task.strip()})
        except Exception as e:
            # Even if an insertion error occurs, redirect or handle safely
            print(f"Error inserting task: {e}")

    return redirect("/")


if __name__ == "__main__":
    # Local development server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
