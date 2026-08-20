from flask import Flask, request
from research_tools import (
    search_papers,
    generate_study_plan,
    add_to_collection,
    mark_completed,
    save_note
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    study_plan = []
    search_results = []

    collection_message = ""
    progress_message = ""
    note_message = ""

    analytics = {
        "learning_goals": 3,
        "collections": 1,
        "reading_progress": 1,
        "notes": 2
}
    
    if request.method == "POST":

        action = request.form.get("action")

        if action == "study_plan":

            goal = request.form.get("goal", "")

            if goal:
                study_plan = generate_study_plan(goal)

        elif action == "search":

            query = request.form.get("query", "")

            if query:
                search_results = search_papers(query)

        elif action == "collection":

            collection_name = request.form.get("collection_name")
            paper_id = request.form.get("paper_id")

            collection_message = add_to_collection(
                collection_name,
                paper_id
            )

        elif action == "progress":

            paper_id = request.form.get("completed_paper")

            progress_message = mark_completed(
                paper_id
            )

        elif action == "note":

            note_text = request.form.get("note_text")

            note_message = save_note(
                note_text
            )

    return f"""
<!DOCTYPE html>
<html>

<head>

<title>ResearchGPT</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    margin: 0;
}}

.header {{
    background: #1f4e79;
    color: white;
    text-align: center;
    padding: 25px;
}}

.container {{
    width: 90%;
    margin: auto;
    padding: 20px;
}}

.card {{
    background: white;
    margin-bottom: 20px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

h2 {{
    color: #1f4e79;
}}

input, textarea {{
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
}}

button {{
    background: #1f4e79;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 5px;
    cursor: pointer;
}}

button:hover {{
    background: #163a5c;
}}

.message {{
    margin-top: 10px;
    color: green;
    font-weight: bold;
}}

.placeholder {{
    color: gray;
}}

</style>

</head>

<body>

<div class="header">
    <h1>ResearchGPT</h1>
    <p>Research Paper Discovery, Study Planning, and Progress Tracking</p>
</div>

<div class="container">

    <div class="card">

        <h2>Learning Goal</h2>

        <form method="POST">

            <input
                type="text"
                name="goal"
                placeholder="Enter your learning goal">

            <button
                type="submit"
                name="action"
                value="study_plan">
                Generate Study Plan
            </button>

        </form>

    </div>

    <div class="card">

        <h2>Research Paper Search</h2>

        <form method="POST">

            <input
                type="text"
                name="query"
                placeholder="Search research papers">

            <button
                type="submit"
                name="action"
                value="search">
                Search Papers
            </button>

        </form>

    </div>

    <div class="card">

        <h2>Study Plan</h2>

        {
            "<ul>" + "".join(
                [
                    f"<li>Day {item['day']}: {item['paper']} ({item['citation']})</li>"
                    for item in study_plan
                ]
            ) + "</ul>"
            if study_plan
            else '<p class="placeholder">No study plan generated yet.</p>'
        }

    </div>

    <div class="card">

        <h2>Search Results</h2>

        {
            "<ul>" + "".join(
                [
                    f'''
                    <li>
                    <strong>{paper["title"]}</strong><br>
                    Year: {paper["year"]}<br>
                    Citations: {paper["citations"]}<br>
                    Paper ID: {paper["paper_id"]}
                    </li><br>
                    '''
                    for paper in search_results
                ]
            ) + "</ul>"
            if search_results
            else '<p class="placeholder">No search results yet.</p>'
        }

    </div>

    <div class="card">

        <h2>Collections</h2>

        <form method="POST">

            <input
                type="text"
                name="collection_name"
                placeholder="Collection Name">

            <input
                type="text"
                name="paper_id"
                placeholder="Paper ID">

            <button
                type="submit"
                name="action"
                value="collection">
                Add Paper
            </button>

        </form>

        <div class="message">
            {collection_message}
        </div>

    </div>

    <div class="card">

        <h2>Reading Progress</h2>

        <form method="POST">

            <input
                type="text"
                name="completed_paper"
                placeholder="Paper ID">

            <button
                type="submit"
                name="action"
                value="progress">
                Mark Completed
            </button>

        </form>

        <div class="message">
            {progress_message}
        </div>

    </div>

    <div class="card">

        <h2>Research Notes</h2>

        <form method="POST">

            <textarea
                rows="5"
                name="note_text"
                placeholder="Enter notes about a paper"></textarea>

            <button
                type="submit"
                name="action"
                value="note">
                Save Note
            </button>

        </form>

        <div class="message">
            {note_message}
        </div>

    </div>

    <div class="card">

    <h2>Analytics Dashboard</h2>

    <p>
        <strong>Learning Goals Created:</strong>
        {analytics["learning_goals"]}
    </p>

    <p>
        <strong>Collections Created:</strong>
        {analytics["collections"]}
    </p>

    <p>
        <strong>Reading Progress Updates:</strong>
        {analytics["reading_progress"]}
    </p>

    <p>
        <strong>Notes Saved:</strong>
        {analytics["notes"]}
    </p>

</div>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)