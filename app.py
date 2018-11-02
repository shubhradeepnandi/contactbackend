from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL

#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'sampdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/')
def main():
    return render_template('signup.html')


@app.route('/data',methods=['POST','GET'])
def data():
    try:
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        requirement = request.form['requirement']

        # validate the received values
        if name and email and phone_number and requirement :
            
            # All Good, let's call MySQL



            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('profile',(name,email,phone_number,requirement))
            #cursor.execute('INSERT INTO profile(name, email, phone_number, requirement) VALUES (%s,%s,%s,%s)',(name, email, phone_number, requirement))
            data = cursor.fetchall()
            print(data[0])

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run(port=5004)
