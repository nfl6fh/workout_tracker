# Workout Tracker

This is a Django-based website that allows users to upload workout plans and track their workout results.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/workout_tracker.git
    ```

2. Change into the project directory:

    ```bash
    cd workout_tracker
    ```

3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    - For macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

    - For Windows:

      ```bash
      venv\Scripts\activate
      ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run database migrations:

    ```bash
    python manage.py migrate
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. Open your web browser and visit `http://localhost:8000` to access the website.

## Usage

- Register a new account or log in if you already have one.
- Upload your workout plans and track your workout results.
- Explore other users' workout plans for inspiration.

## Contributing

Contributions are welcome! If you have any suggestions or find any issues, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
