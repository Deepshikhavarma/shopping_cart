import psycopg2
import pandas as pd

con = psycopg2.connect(database="postgres", user='deepshikha', password='postgres', host='127.0.0.1', port= '5432'
)

con.autocommit = True

#Creating a cursor object using the cursor() method
cursor = con.cursor()
#
try:
    connection = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1', port= '5432')
    print('Database connected.')
except:
    sql = '''CREATE database Shopuser5''';
    cursor.execute(sql)
    con.commit()
    conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1', port= '5432'
    )
    cursor = conn.cursor()
    sql ='''CREATE TABLE USERS1(
       EMAIL_ID CHAR(30) NOT NULL,
       PASSWORD CHAR(30) NOT NULL
    )'''
    sql1 = '''CREATE TABLE CART(
        Product_ID INTEGER NOT NULL,
        Product_Name CHAR(10) NOT NULL
        )'''

    sql2 = '''CREATE TABLE ORDER_HISTORY(
        Product_ID INTEGER NOT NULL,
        Product_Name CHAR(10) NOT NULL
        )'''
    sql3 = '''CREATE TABLE PRODUCTS(Product_ID INTEGER NOT NULL,
        Product_Name CHAR(10) NOT NULL
        )'''
    cursor.execute(sql)
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    user_insert_query = """ INSERT INTO USERS1 (EMAIL_ID, PASSWORD) VALUES ('admin', 'admin'),('Deepshikha', '1234')"""
    product_insert_query = """ INSERT INTO PRODUCTS (Product_ID, Product_Name) VALUES (1, 'Desktop'),(2, 'EarPods'),
    (3, 'Power Bank'),(4, 'Mouse'),(5, 'Keyboard')"""
    cursor.execute(user_insert_query)
    cursor.execute(product_insert_query)

    conn.commit()

#Closing the connection
con.close()


def UserLogin():
    username = input("Username:" )
    password = input("Password:" )
    conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1', port='5432'
                            )
    cursor = conn.cursor()
    query = "select * from USERS1"
    cursor.execute(query)
    data = cursor.fetchall()
    for x in data:
        un = x[0].split(" ")
        pwd = x[1].split(" ")
        if un[0] == username and pwd[0] == password:
            print("Successfully Logged In")
            if username == 'admin' and password == 'admin':
                admin_input()

            else:
                user = 'user'
                ShowItems(user)
        else:
            print("Invalid Username or Password")


def admin_input():
    user = "admin"
    print("Type P to see all products")
    print("Type I to add products")
    print("Type D to remove product")
    print("Type R to print report")
    admin_inst = input("Type Your Instruction:")
    if admin_inst == "P":
        ShowItems(user)
        admin_input()
    elif admin_inst == "I":
        add_product()
    elif admin_inst == "D":
        delete_product()
    elif admin_inst == "R":
        report()
    else:
        print("Entered Wrong Value")

def add_product():
    conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1',
                            port='5432')
    cursor = conn.cursor()
    ids = """SELECT Product_ID from PRODUCTS"""
    cursor.execute(ids)
    ids = cursor.fetchall()
    list_id=[]
    for x in ids:
        list_id.append(int(x[0]))

    product_name = input("Enter Product:" )
    product_insert_query = """ INSERT INTO PRODUCTS (Product_ID, Product_Name) VALUES (%s, %s)"""
    record_to_insert = (list_id[-1]+1, product_name)
    cursor.execute(product_insert_query, record_to_insert)
    conn.commit()
    print(product_name, "Added Succesfully!")
    add_more = input("Add more Product? Yes or No: ")
    if add_more == "Yes":
        add_product()
    elif add_more == "No":
        admin_input()
    else:
        print("Wrong Input")


def delete_product():
    ShowItems()
    input_id = input("Enter Product Id you want to delete: ")
    del_product= """DELETE FROM PRODUCTS WHERE Product_ID = %s"""
    cursor.execute(del_product, input_id)
    conn.commit()
    print("Product Deleted Successfully!")
    delete_more = input("Delete more Producr? Yes or No: ")
    if delete_more == "Yes":
        delete_product()
    elif delete_more == "No":
        admin_input()
    else:
        print("Entered Wrong Value")


def report():
    conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1',
                            port='5432')
    cursor = conn.cursor()
    prod = """SELECT * FROM ORDER_HISTORY"""
    cursor.execute(prod)
    prod = cursor.fetchall()
    ids = []
    product = []
    for x in prod:
        ids.append(int(x[0]))
        product.append(x[1])
    data = {'ID': ids,
            'Product': product}
    df = (pd.DataFrame(data)[['ID', 'Product']])
    df.set_index('ID', inplace=True)
    print(df)

def ShowItems(user):
    p_user = user
    conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1', port='5432'
                            )
    cursor = conn.cursor()
    query = "select * from PRODUCTS"
    cursor.execute(query)
    data = cursor.fetchall()
    for x in data:
        print(f'{x[0]} {x[1]}')
    if p_user == 'admin':
        admin_input()
    else:
        user_inputs()

def user_inputs():
    print("Type A to add products in cart")
    print("Type B to see order history")
    print("Type X to exit")
    userinput = input("Type Your Instruction:")
    if userinput == "A":
        produts = input("Add Product ID written in front of product:" )
        products = produts.split(",")
        conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1',
                                port='5432')
        cursor = conn.cursor()
        prod = """SELECT * FROM PRODUCTS"""
        cursor.execute(prod)
        prod = cursor.fetchall()
        for x in prod:
            for y in products:
                if str(x[0]) == y:
                    cart_insert_query = """ INSERT INTO CART (Product_ID, Product_Name) VALUES (%s, %s)"""
                    record_to_insert = (x[0],x[1])
                    cursor.execute(cart_insert_query,record_to_insert)

        conn.commit()
        buy = input("Do you want to buy these selected producs? Yes or No: ")
        if buy=="Yes":
            conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1',
                                    port='5432')
            cursor = conn.cursor()
            prod = """SELECT * FROM CART"""
            cursor.execute(prod)
            prod = cursor.fetchall()
            for x in prod:
                order_insert_query = """ INSERT INTO ORDER_HISTORY (Product_ID, Product_Name) VALUES (%s, %s)"""
                record_to_insert = (x[0], x[1])
                cursor.execute(order_insert_query, record_to_insert)
            conn.commit()
            print("Order Placed")
            user_inputs()
        elif buy=="No":
            user_inputs()
        else:
            print("Wrong Input")

    elif userinput == "B":
        buy_product()

    elif userinput == "X":
        quit()

    else:
        print("Wrong Value Entered")


def buy_product():
    conn = psycopg2.connect(database="shopuser5", user='deepshikha', password='postgres', host='127.0.0.1',
                            port='5432')
    cursor = conn.cursor()
    prod = """SELECT * FROM ORDER_HISTORY"""
    cursor.execute(prod)
    prod = cursor.fetchall()
    print("Your Ordered Products are:")
    for x in prod:
        print(x[1])

    user_inputs()

UserLogin()
