from fastapi import FastAPI, Form, File, UploadFile
from typing import Optional
import pandas as pd
from fuzzywuzzy import process  # Import for fuzzy matching

app = FastAPI()

# Path to your CSV file
csv_file_path = "./data.csv"

@app.post("/api/")
async def get_answer(
    question: str = Form(...),
    file: Optional[UploadFile] = None
):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Get the column with questions from the CSV
        questions_list = df['question'].tolist()

        # Use fuzzy matching to find the best match for the given question
        best_match, score = process.extractOne(question, questions_list)

        # Define a similarity threshold (e.g., 80)
        if score > 80:  # If the match is sufficiently similar
            # Retrieve the answer for the matched question
            filtered_row = df[df['question'] == best_match]
            return {"answer": filtered_row['answer'].iloc[0]}
        else:
            return {"answer": "Question not found with sufficient similarity"}

    except Exception as e:
        return {"answer": f"Error reading the CSV file: {e}"}