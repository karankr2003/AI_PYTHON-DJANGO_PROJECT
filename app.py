from flask import Flask, request, jsonify
import cohere
import mysql.connector

app = Flask(__name__)

COHERE_API_KEY = "api key"
co = cohere.Client(api_key=COHERE_API_KEY)

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "mysql"
DB_NAME = "employees"

@app.route('/generate-query', methods=['POST'])
def generate_query():
    data = request.json
    user_content = data.get("prompt")

    response = co.generate(
        model="command-xlarge-nightly",
        prompt=user_content,
        max_tokens=100,
        temperature=0.7,
        stop_sequences=["--"],
    )

    sql_query = response.generations[0].text.strip()
    return jsonify({"sql_query": sql_query})

@app.route('/execute-query', methods=['POST'])
def execute_query():
    data = request.json
    sql_query = data.get("sql_query")

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

        return jsonify({"columns": column_names, "rows": result})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})

if __name__ == '__main__':
    app.run(debug=True)
