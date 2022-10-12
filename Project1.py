# ~~~~~~~~~~~~~~ Imports ~~~~~~~~~~~~~~ #
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
# ~~~~~~~~~~~~~~ Imports ~~~~~~~~~~~~~~ #
# ~~~~~~~~~ Flask Initialization ~~~~~~~~~ #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TheLibrary.sqlite3'
app.config['SECRET_KEY'] = "The Library of Alon"

db = SQLAlchemy(app)
# ~~~~~~~~~ Flask Initialization ~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~ TheLibrary Build ~~~~~~~~~~~~~~~~ #

# TODO: Watch October 9th class and research documentation of SQLAlchemy ("https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/")

# ~~~~~~~~~~~ Client Class ~~~~~~~~~~~ #
class Customers(db.Model):
    ID = db.Column('CustomerID', db.Integer, primary_key = True)
    Name = db.Column('CustomerName', db.String(50))
    Age = db.Column('CustomerAge', db.Integer)
    City = db.Column('CustomerCity', db.String(25))
    Status = db.Column('CustomerActive', db.Integer)
    LoanLink = db.relationship("Loan", backref = "customers", lazy = True)

    def __init__(self, Name, Age, City, Status):
        self.Name = Name
        self.Age = Age
        self.City = City
        self.Status = Status
# ~~~~~~~~~~~ Client Class ~~~~~~~~~~~ #

# ~~~~~~~~~~~ Books Class ~~~~~~~~~~~ #
class Books(db.Model):
    ID = db.Column('BookID', db.Integer, primary_key = True)
    Name = db.Column('BookName', db.String(100))
    Author = db.Column('BookAuthor', db.String(50))
    Published = db.Column('PublishedDate', db.String(10))
    Type = db.Column('BookType', db.Integer)
    LoanLink = db.relationship("Loan", backref = "books", lazy = True)

    def __init__(self, Name, Author, Published, Type):
        self.Name = Name
        self.Author = Author
        self.Published = Published
        self.Type = Type
# # ~~~~~~~~~~~ Books Class ~~~~~~~~~~~ #

# ~~~~~~~~~~~~ Loan Class ~~~~~~~~~~~~ #
class Loan(db.Model):
    ID = db.Column('LoanID', db.Integer, primary_key = True)
    CustomerID = db.Column('CustomerID', db.Integer, db.ForeignKey("customers.CustomerID"))
    BookID = db.Column('BookID', db.Integer, db.ForeignKey("books.BookID"))
    LoanDate = db.Column('LoanDate', db.String(10))
    ReturnDate = db.Column('ReturnDate', db.String(10))

    def __init__(self, CustomerID, BookID, LoanDate, ReturnDate):
        self.CustomerID = CustomerID
        self.BookID = BookID
        self.LoanDate = LoanDate
        self.ReturnDate = ReturnDate
# ~~~~~~~~~~~~ Loan Class ~~~~~~~~~~~~ #

# ~~~~~~~~~~~~ Operator's Options ~~~~~~~~~~~~ #
@app.route("/")
def home():
    return "Welcome!"

@app.route('/Customers/<Name>')
@app.route('/Customers/', methods = ['GET'])
def AllCustomers(Name = ""):
    CustomerList = []
    for Customer in Customers.query.all():
    # FIXME: Check if code is true and functional. 
        # if Name == Customers.Name:
        #     SingleCustomer = Customers.query.all(Customers.Name == str(Name))
        #     return {"ID": SingleCustomer.ID, "Name": SingleCustomer.Name, "Age": SingleCustomer.Age, "City": SingleCustomer.City, "Status": SingleCustomer.Status}
        if (Customer.Name == Name): 
            SingleCustomer = Customers.query.all(Customers.Name == str(Name))
            return {"ID": SingleCustomer.ID, "Name": SingleCustomer.Name, "Age": SingleCustomer.Age, "City": SingleCustomer.City, "Status": SingleCustomer.Status}
        else:
            CustomerList.append({"ID": Customer.ID, "Name": Customer.Name, "Age": Customer.Age, "City": Customer.City, "Status": Customer.Status})
            return CustomerList

@app.route('/Customers/add', methods = ['POST'])
def AddCustomer():
    requestData = request.get_json()
    Name = requestData ['Name']
    Age = requestData ['Age']
    City = requestData ['City']
    Status = requestData ['Status']

    newCustomer = Customers(Name, Age, City, Status)
    db.session.add(newCustomer)
    db.session.commit()
    return f"Customer '{newCustomer.Name}' created."

@app.route('/Books/', methods = ['GET'])
def AllBooks():
    BookList = []
    for Book in Books.query.all():
        BookList.append({"ID": Book.ID, "Name": Book.Name, "Author": Book.Author, "Published": Book.Published, "Type": Book.Type})
    return BookList

@app.route('/Books/add', methods = ['POST'])
def AddBook():
    requestData = request.get_json()
    Name = requestData ['Name']
    Author = requestData ['Author']
    Published = requestData ['Published']
    Type = requestData ['Type']

    newBook = Books(Name, Author, Published, Type)
    db.session.add(newBook)
    db.session.commit()
    return f"Book '{newBook.Name}' added."
# ~~~~~~~~~~~~ Operator's Options ~~~~~~~~~~~~ #


# ~~~~~~~~~~~~~~~~ TheLibrary Build ~~~~~~~~~~~~~~~~ #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)