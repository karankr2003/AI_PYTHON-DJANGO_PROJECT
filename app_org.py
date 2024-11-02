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
    "employeess": ["emp", "employee", "staff", "workers","employees"],
    "departments": ["divisions", "sections", "depart","department"],
}

def fetch_metadata():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s", (DB_NAME,))
    tables = cursor.fetchall()
    
    metadata = {}
    for (table_name,) in tables:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s", (DB_NAME, table_name))
        columns = cursor.fetchall()
        metadata[table_name] = [column[0] for column in columns]

    cursor.close()
    connection.close()
    
    return metadata

def translate_synonyms(prompt):
    for table, syns in synonyms.items():
        #print(table)
        #print(syns)
        for syn in syns:
            prompt = prompt.replace(syn, table)
    return prompt

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-query', methods=['POST'])
def generate_query():
    user_content = request.json.get('prompt')
    translated_content = translate_synonyms(user_content)
    metadata = fetch_metadata()
    
    metadata_str = "Tables and columns in the database:\n"
    for table, columns in metadata.items():
        metadata_str += f"Table: {table}, Columns: {', '.join(columns)}\n"
    
    full_prompt = f"{metadata_str}\nUser Query: {translated_content}"
    
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
