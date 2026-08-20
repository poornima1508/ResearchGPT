collections = []
progress = []
notes = []


def search_papers(query, top_k=5):

    return [
        {
            "paper_id": "W001",
            "title": f"Research Paper About {query}",
            "year": 2024,
            "citations": 150
        },
        {
            "paper_id": "W002",
            "title": f"Advanced Topics in {query}",
            "year": 2023,
            "citations": 95
        },
        {
            "paper_id": "W003",
            "title": f"Modern Methods for {query}",
            "year": 2022,
            "citations": 72
        }
    ]


def generate_study_plan(goal):

    papers = search_papers(goal)

    plan = []

    for day, paper in enumerate(papers, start=1):

        plan.append({
            "day": day,
            "paper": paper["title"],
            "citation": paper["paper_id"]
        })

    return plan


def add_to_collection(collection_name, paper_id):

    collections.append({
        "collection": collection_name,
        "paper_id": paper_id
    })

    return f"Paper {paper_id} added to {collection_name}"


def mark_completed(paper_id):

    progress.append(paper_id)

    return f"Paper {paper_id} marked completed"


def save_note(note_text):

    notes.append(note_text)

    return "Note saved successfully"
