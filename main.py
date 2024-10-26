import json
import requests
import os

def load_start_index(file_path):
    """Loads the start index from a file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return int(f.read().strip())
    return 0

def save_start_index(file_path, index):
    """Saves the current start index to a file."""
    with open(file_path, 'w') as f:
        f.write(str(index))

def post_mcq_to_facebook(access_token, question):
    """Posts the MCQ to Facebook using the Graph API."""
    mcq_text = f"{question['question']}\n" + '\n'.join(question['options'])
    url = "https://graph.facebook.com/v17.0/me/feed"

    response = requests.post(
        url,
        params={"message": mcq_text, "access_token": access_token}
    )

    if response.status_code == 200:
        print(f"Successfully posted question!")
    else:
        print(f"Failed to post: {response.status_code} {response.text}")

def main():
    # Load the access token from environment variables
    access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

    start_index_file = "start_index.txt"

    # Load questions from the JSON file
    with open('questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # Load or initialize the start index
    start_index = load_start_index(start_index_file)

    # Ensure the index wraps around if all questions are posted
    if start_index >= len(questions):
        start_index = 0

    # Post the current question
    question = questions[start_index]
    post_mcq_to_facebook(access_token, question)

    # Save the updated start index
    save_start_index(start_index_file, start_index + 1)

if __name__ == "__main__":
    main()
