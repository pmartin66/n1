from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import socket


app = Flask(__name__)
DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
#COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
#DBPORT = int(os.environ.get("DBPORT"))
My_name = os.environ.get('MYNAME')
image_url=os.environ.get('image_url')
#if os.path.exists('/clo835/config/image_url'):
 #My_file = open("/clo835/config/image_url", "r")
 #image_url = My_file.read()
 #print("Background image url is ",image_url)

# Create a connection to the MySQL database
###db_conn = connections.Connection(
    #host= DBHOST,
    #port=DBPORT,
    #user= DBUSER,
    #password= DBPWD, 
    #db= DATABASE
    
    #)
output = {}
table = 'employee';

# Define the supported color codes
#color_codes = {
#    "red": "#e74c3c",
#    "green": "#16a085",
#    "blue": "#89CFF0",
#    "blue2": "#30336b",
#    "pink": "#f4c2c2",
#    "darkblue": "#130f40",
#    "lime": "#C1FF9C",
#}

# Generate a random color
#COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])

    
@app.route("/", methods=['GET','POST'])
def main():
   return render_template('addemp.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set") )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, background=bg_codes[bg])

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", background=bg_codes[bg])


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], background=bg_codes[bg])

if __name__ == '__main__':
    
    # Check for Command Line Parameters for bg
    parser = argparse.ArgumentParser()
    parser.add_argument('--bg', required=False)
    args = parser.parse_args()

    if args.bg:
        print("bg from command line argument =" + args.bg)
        bg = args.bg
        if BACK_ENV:
            print("A bg was set through environment variable -" + BACK_ENV + ". However, bg from command line argument takes precendence.")
    elif BACK_ENV:
        print("No Command line argument. bg from environment variable =" + BACK_ENV)
        bg = BACK_ENV
    else:
        print("No command line argument or environment variable. Picking a Random bg =" + bg)

    # Check if input color is a supported one
    if bg not in bg_codes:
        print("bg not supported. Received '" + bg + "' expected one of " + SUPPORTED_BG)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)
