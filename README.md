# Email Processing and Embedding Generation System

This project is designed to fetch emails using Gmail API, process them to generate initial embeddings, and serve these functionalities through an API.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip

## Setup

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Make sure you have the `credentials.json` file from Google Cloud. This should be of type "Desktop" for OAuth2.

4. Run the `gmails.py` script to authenticate and fetch emails:

    ```bash
    python gmails.py
    ```

    - Complete the SSO authentication process to allow access to your Gmail.
    - This will generate the `emails.jsonl` file containing the fetched emails.

## Running the System

1. Start the Python server:

    ```bash
    python server.py
    ```

2. In another terminal window, start Ollama:

    ```bash
    ollama serve
    ```

## API Endpoints

### Health Check

- **Endpoint:** `GET /`
- **Description:** Check if the server is running.

### Process Emails

- **Endpoint:** `GET /process_emails`
- **Description:** Process the email data, create embeddings, and ensure to remove big garbage emails from `emails.jsonl`.

### Ask a Question

- **Endpoint:** `GET /ask`
- **Query Parameter:** `q` - The question string.
- **Description:** Ask a question based on the processed email data.

## Observer Pattern

In the real system, email processing and embedding generation will be triggered upon user registration following the observer pattern.

## Notes

- Ensure `credentials.json` is correctly configured and available in the project directory.
- `emails.jsonl` will be generated after running the initial `gmails.py` script.

## Example Usage

1. Check the server health:

    ```bash
    curl localhost:3000/
    ```

2. Process emails to create embeddings:

    ```bash
    curl localhost:3000/process_emails
    ```

3. Ask a question:

    ```bash
    curl "localhost:3000/inquire?q=What is the subject of the last email?"
    ```

## License

This project is licensed under the MIT License.
