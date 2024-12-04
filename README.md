# SQL Code Generator Using AI
Web Application

## Project Details

**Languages**: Python, AI, Django, HTML, CSS

**Database**: MySQL

SQLAlchemyAI is a Python and Django-based web application that converts natural language inputs into SQL queries using AI.

### Key Features
- **Natural Language Processing (NLP)**: Leverages advanced NLP techniques to interpret user inputs and generate corresponding SQL queries.
- **User-Friendly Interface**: Allows users to interact with their databases effortlessly, simplifying complex queries and routine operations.
- **Enhanced Productivity**: Streamlines database management tasks, making them more intuitive and efficient.
- **Accurate Query Generation**: Ensures precise and accurate results by generating exact SQL queries based on the database schema.

### Technical Overview
- **Backend**: Python with Django framework
- **Frontend**: HTML and CSS for a responsive and user-friendly interface
- **Database Interaction**: MySQL for data storage and management
- **AI Integration**: Utilizes machine learning models to translate natural language into SQL

## Installation and Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/karankr2003/SQLAlchemyAI.git
    ```
2. Navigate to the project directory:
    ```sh
    cd SQLAlchemyAI
    ```
3. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Configure the database settings in `settings.py`:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

7. Start the development server:
    ```sh
    python app.py
    ```

## Usage
1. Access the web application by navigating to `http://127.0.0.1:8000` in your web browser.
2. Enter a natural language query in the input box.
3. The AI will process the input and generate the corresponding SQL query.
4. Review and execute the generated SQL query on your database.

## Contributing
We welcome contributions to enhance the SQLAlchemyAI project. If you would like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.


## Contact
For any inquiries or support, please contact [karankumar496kk@gmail.com].

