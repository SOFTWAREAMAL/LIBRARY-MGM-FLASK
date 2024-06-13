from flask import Flask,request,render_template,redirect,url_for
from mysql.connector import * 
mysql=connect(
    host = "localhost",
    user = "root",
    password = "amalan",
    database = "library")

cursor = mysql.cursor(dictionary=True)
create = """
        create table library
        ( 
        book_name varchar(50),
        student_name varchar(50),
        issue_date varchar(20),
        return_date varchar(20)
        );
        """
#cursor.execute(create)
print("success create table")

app=Flask(__name__)

@app.route('/home_page') 
def home_page():
    return render_template('homepage.html')

admin_dict={"admin":"123"}
    
@app.route('/',methods=["POST","GET"])
def admin_login():
    if request.method == "POST":
        ad_name = request.form["admin_name"]
        ad_pw = request.form["admin_password"]
     
        if ad_name == 'admin' and ad_pw == '123':
             return render_template('homepage.html')
        else:
            return  "<h1> Invalid </h1>"
    return render_template('admin_login.html')

@app.route('/add_book',methods=["POST","GET"])
def add_book():
    if request.method == "POST":
        b_name = request.form.get("book_name")
        ad_pw = request.form["admin_password"]     
       
        insert = """
                insert into library(book_name) value(%s);
                """
        i = (b_name)
        cursor.execute(insert,i)
        mysql.commit()  
       
        cursor.execute('select book_name from library where book_name = %s ',(b_name,))
        result = cursor.fetchone()
        print(result)
        if result and ad_pw == '123':
            #mysql.commit()
            return f"<h1> BOOK {result} IS ADDED BY ADMIN ! </h1>"
        else:
            return f"<h1> SORRY  BOOK {result} IS NOT ADDED </h1>"
    return render_template ('add_book.html')



@app.route('/check_book_availability',methods=["POST","GET"])
def check_book_availability():
    if request.method == "POST":
        b_name = request.form.get("book_name")
        ad_pw = request.form["admin_password"]     
       
        cursor.execute('select book_name from library where book_name = %s ',(b_name,))
        result = cursor.fetchone()
        print(result)
        if result and ad_pw == '123':
            #mysql.commit()
            return f"<h1> BOOK IS AVAILABLE {result} ! </h1>"
        else:
            return f"<h1> SORRY  BOOK {result} IS NOT AVAILABLE </h1>"
    return render_template ('check_book_availability.html')

@app.route('/issue_book', methods=["POST","GET"])
def issue_book():
    if request.method == "POST":
        ad_pw = request.form.get("admin_password")     
        b_name = request.form.get("book_name")
        s_name = request.form.get("student_name")
        is_dt = request.form.get("issue_date")     
        re_dt = request.form.get("return_date")             
           
        insert = """
            insert into student(book_name,student_name,issue_date,return_date) values(%s,%s,%s,%s);
            """
        i = (b_name,s_name,is_dt,re_dt)
        cursor.execute(insert,i)
        result=cursor.fetchone()
        print(result)
        if ad_pw == '123':
            cursor.execute('DELETE FROM library where book_name = %s',(b_name,))
            mysql.commit()
            return f"<h1> book issued to student ! {result} </h1>" 
        else:
            return "Invalid admin_password "
    return render_template('issue.html')

@app.route('/return_book', methods=["POST","GET"])
def return_book():
    if request.method == "POST":
        ad_pw = request.form.get("admin_password")     
        b_name = request.form.get("book_name")
        s_name = request.form.get("student_name")
        re_dt = request.form.get("return_date")
        s_re_dt = request.form.get("student_return_date")             
           
        cursor.execute('update student set student_return_date = %s where book_name = %s and student_name = %s',(s_re_dt,b_name,s_name))
        cursor.execute('select return_date from student where return_date > student_return_date and book_name = %s and student_name = %s',
        (b_name,s_name))
        
        result=cursor.fetchone()
        print(result)
        if ad_pw == '123' and result:
            insert = "insert into library (book_name) values(%s); "
            i = (b_name,)
            cursor.execute(insert,i)
            mysql.commit()
            return  "<h1> Student return the book successful! </h1>" 
        
        else:
            return "<h1> Pay fine amount Rs.100 <h1>"
    return render_template('return.html')


if __name__ == "__main__":
    app.run(debug=True)

cursor.close()
mysql.close()