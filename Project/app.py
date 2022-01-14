# MODULES REQURIED 
from flask_mysqldb import MySQL
import mysql.connector
import random
from flask import Flask, render_template, request, abort
# CREATING FLASK APP
app = Flask(__name__)
 
# ERROR PAGE FUNCTION 
@app.route('/404Error')
def error():
    abort(401)
 
# MYSQL CONFIGURATION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Error404' 
app.config['MYSQL_DB'] = 'grocery'
 

mysql = MySQL(app)

# HOME PAGE
@app.route('/')
def index():
    return('This is the current home page of mmy project.')

# A RANDOM SERIAL NUMBER FOR ORDERING 
global num
num = random.random()

# WHEN ORDER IS FINSIHED
@app.route('/done')
def done():
    return render_template('end.html')

# VARIABLE FOR THE TOTAL AMOUNT TO BE DISPLAYED IN THE END
total_amount = []

# PAGE FOR THE ORDERING 
@app.route('/order',methods=['GET', 'POST'])
def order():
    # CONNECTION
    cur = mysql.connection.cursor()
    # ASSIGNING VARIABLES 
    gcode = 0
    pqty = 0 
    if request.method == "POST":
        # GETTING VARIABLE INPUTED BY THE USER
        gcode = request.form['code']
        pqty = request.form['qty']
        
    
    
    cur.execute(f"select gcode, gname, gprice * {pqty} from product where gcode = {gcode}")
    recor = cur.fetchall()
    custdict = []
    
    for i in recor:
        #newdict = {'CODE':i[0],'NAME': i[1],'QUANTITY': i[2],'PRICE': i[3]}
        code = i[0]
        name = i[1]
        quantity = pqty
        price = i[2]
        
        total_amount.append(price)
        cur.execute(f"insert into order_prod values('{num}',{code},'{name}',{quantity}, '{price}');")
        # IF THE QUNATITY OF THE PRODUCT TABLE IS NULL
        #THE FUNCTION DOESN'T STOP AS NULL - {QUNATITY} = NULL
        sql = (f"update product set pqty = pqty - {quantity} where gcode = {code}; ")
        cur.execute(sql)

    cur.execute(f"select * from order_prod where num = '{num}';")
    tyu = cur.fetchall()
    

    for m in tyu:
        ui = {'CODE': m[1],'NAME' : m[2], 'QUANTITY' :m[3], 'PRICE': m[4]}    
        custdict.append(ui)

    print(total_amount)
    new_amount = 0
    for q in total_amount:
         new_amount += q

    mysql.connection.commit()
    cur.close()
    return render_template('order.html',ord=custdict,amount = new_amount)

#PRODUCT PAGE 
@app.route('/prod_items', methods=['GET', 'POST'])
def prod_items():
    
    cur = mysql.connection.cursor()
    cur.execute('select * from product;')
    records = cur.fetchall()
    big_dict = []
    # reading from student file one by one
    for row in records:
        if row[3] > 0:
            dict = {'CODE': row[0],'NAME' : row[1], 'PRICE' :row[2], 'QUANTITY': row[3]}    
            big_dict.append(dict)
        else:
            pass
    return render_template('prod.html',prod = big_dict)
     
#LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        login_id = details['id']
        login_pass = details['pass']
        cur = mysql.connection.cursor()
        cur.execute(f"select * from login where login_id = '{login_id}' and login_password = '{login_pass}';")
        records = cur.fetchall()
            
        if len(records) == 1:
            return prod_items()

        if len(records) != 1:
            return error()
        mysql.connection.commit()
        cur.close()

    return render_template('index.html')
  
if __name__ == '__main__':
    app.run()

user_ans = input("Setup: Want to set up the database: Y/N:")
if user_ans.lower() == "y":
    conn = mysql.connector.connect(host="localhost", user="root", passwd="@Error404", database="grocery")
    mycursor = conn.cursor()
    #PRODUCT TABLE
    mycursor.execute("CREATE TABLE if not exists product (gcode int(4) PRIMARY KEY,gname char(30) NOT NULL, gprice float(8,2)NOT NULL,pqty int(5))")
    print("PRODUCT table created\n")
    #LOGIN TABLE
    mycursor.execute("CREATE TABLE if not exists login(cid char(6) PRIMARY KEY,login_id char(50) NOT NULL,login_password char(50) NOT NULL) ;")
    print("LOGIN table created\n")
else:
    pass
