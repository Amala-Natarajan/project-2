from fastapi import FastAPI, Form, UploadFile
from typing import Optional
import pandas as pd
import os
from fuzzywuzzy import process  # Fuzzy matching for question lookup

app = FastAPI()

# Absolute path to the CSV file
csv_file_path = os.path.abspath("./data.csv")

@app.post("/api/")
async def get_answer(
    question: str = Form(...),
    file: Optional[UploadFile] = None
):
    if not question.strip():
        return {"answer": "Invalid input: question cannot be empty."}

    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Check if required columns exist
        if 'question' not in df.columns or 'answer' not in df.columns:
            return {"answer": "Error: CSV file must contain 'question' and 'answer' columns."}

        # Ensure non-empty data
        if df.empty:
            return {"answer": "Error: CSV file is empty."}

        # Get the column with questions from the CSV
        questions_list = df['question'].dropna().tolist()

        # Use fuzzy matching to find the best match for the given question
        best_match, score = process.extractOne(question, questions_list) if questions_list else (None, 0)

        # Define a similarity threshold (e.g., 80)
        if best_match and score > 80:
            filtered_row = df[df['question'] == best_match]
            return {"answer": filtered_row['answer'].iloc[0]}
        else:
            return {"answer": "Question not found with sufficient similarity."}

    except Exception as e:
        return {"answer": f"Error processing the request: {e}"}
