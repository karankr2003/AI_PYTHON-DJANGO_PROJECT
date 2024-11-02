import cohere
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
COHERE_API_KEY = "api key"
co = cohere.Client(api_key=COHERE_API_KEY)

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "mysql"
DB_NAME = "employees"

table_schema = {
    "employees": {
        "employee_id": "ID of the employee",
        "first_name": "First name of the employee",
        "last_name": "Last name of the employee",
        "age": "Age of the employee",
        "department": "Department of the employee",
        "salary": "Salary of the employee",
        "hire_date": "Hire date of the employee"
    },
    "departments": {
        "department_id": "ID of the department",
        "department_name": "Name of the department",
        "manager_name": "Name of the manager"
    }
}

synonyms = {
    "employees": ["emp", "employee", "staff", "workers"],
    "departments": ["divisions", "sections", "depart", "department"],
}

def translate_synonyms(prompt):
    for table, syns in synonyms.items():
        for syn in syns:
            prompt = prompt.replace(syn, table)
    return prompt

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-query', methods=['POST'])
def generate_query():
    user_content = request.json.get('prompt')
    print("Original Prompt:", user_content)
    translated_content = translate_synonyms(user_content)
    print("Translated Content:", translated_content)
    
    probable_tables_response = co.generate(
        model="command-xlarge-nightly",
        prompt=f"Suggest probable tables for the query: {translated_content}",
        max_tokens=100,
        temperature=0.7,
        stop_sequences=["--"],
    )
    probable_tables = probable_tables_response.generations[0].text.strip().split(', ')
    print("Probable Tables:", probable_tables)
    
    matched_tables = [table for table in probable_tables if table in table_schema]
    print("Matched Tables:", matched_tables)
    
    response = {
        "matched_tables": matched_tables,
        "columns": {table: table_schema[table] for table in matched_tables}
    }
    
    return jsonify(response)

@app.route('/execute-query', methods=['POST'])
def execute_query():
    user_query = request.json.get('user_query')
    translated_query = translate_synonyms(user_query)
    print("Translated Query:", translated_query)

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(translated_query)
        result = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        cursor.close()
        connection.close()

        return jsonify({"column_names": column_names, "data": result})

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": str(err)})

if __name__ == "__main__":
    app.run(debug=True)
