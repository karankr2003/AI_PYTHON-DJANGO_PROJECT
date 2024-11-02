from flask import Flask, request, jsonify, send_from_directory
import cohere
import mysql.connector

app = Flask(__name__)
COHERE_API_KEY = "api key"
co = cohere.Client(api_key=COHERE_API_KEY)

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "mysql"
DB_NAME = "employees"

synonyms = {
    "employeess": ["emp", "employee", "staff", "workers", "employees"],
    "departments": ["divisions", "sections", "depart", "department"],
}

table_descriptions = {
    "employeess": [
        {"name": "employee_id", "comments": "the id of the employeess"},
        {"name": "first_name", "comments": "the first name of the employeess"},
        {"name": "last_name", "comments": "the last name of the employeess"},
        {"name": "age", "comments": "the age of the employeess"},
        {"name": "department", "comments": "the department of the employeess"},
        {"name": "salary", "comments": "the salary of the employeess"},
        {"name": "hire_date", "comments": "the hire date of the employeess"},
    ],
    "departments": [
        {"name": "department_id", "comments": "the department id of the employeess"},
        {"name": "department_name", "comments": "the department name of the employeess"},
        {"name": "manager_name", "comments": "the manager of the employeess"},
    ],
}
def fetch_metadata():
    return table_descriptions
def translate_synonyms(prompt):
    for table, syns in synonyms.items():
        for syn in syns:
            prompt = prompt.replace(syn, table)
    return prompt

def fetch_existing_data():
    existing_data = {"departments": []}
    existing_data = {"employeess":[]}
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
   
        cursor.execute("SHOW COLUMNS FROM employeess")
        existing_data["employees"] = [row[0] for row in cursor.fetchall()]

        cursor.execute("SHOW COLUMNS FROM departments")
        existing_data["departments"] = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    return existing_data


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-query', methods=['POST'])
def generate_query():
    user_content = request.json.get('prompt')
    translated_content = translate_synonyms(user_content)
    existing_data = fetch_existing_data()

    metadata_str = "Tables and columns in the database:\n"
    for table, columns in fetch_metadata().items():
        metadata_str += f"Table: {table}, Columns: " + ", ".join([f"{col['name']} ({col['comments']})" for col in columns]) + "\n"

    full_prompt = f"{metadata_str}\n Using the above metadata, help me to generate exact sql query for natural langauge prompt + [{translated_content}] + [{fetch_existing_data}] .If the metadeta does not include required table and columns return invalid query"
    print(full_prompt)
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=full_prompt,
        max_tokens=100,
        temperature=0.7,
        stop_sequences=["--"],
    )
    sql_query = response.generations[0].text.strip().replace('\n', ' ')

    return jsonify({"sql_query": sql_query})

@app.route('/execute-query', methods=['POST'])
def execute_query():
    sql_query = request.json.get('sql_query')

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )     
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        cursor.close()
        connection.close()

        return jsonify({"column_names": column_names, "data": result})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})

if __name__ == "__main__":
    app.run(debug=True)
