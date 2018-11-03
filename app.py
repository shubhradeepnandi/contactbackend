from flask import Flask, render_template, request, json
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='username',
                             password='password',
                             db='db',
                             )
app = Flask(__name__)


@app.route("/")
def login():
    return render_template('reg.html')


@app.route('/data', methods=['POST', 'GET'])
def signUp():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        requirement = request.form['requirement']
        try:

            with connection.cursor() as cursor:
                # Read a single record
                sql = "INSERT INTO profile (name,email,phone_number,requirement) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, email, phone_number, requirement))
                connection.commit()
        finally:
            connection.close()
            return json.dumps({'Name': name,
                               'Email': email,
                               'Phone_Number':phone_number,
                               'Requirement':requirement})
    else:
        return "error"


if __name__ == "__main__":
    app.run(port=5040, debug=True)