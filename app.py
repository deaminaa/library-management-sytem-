from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/library_db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Import models from the models.py file
from models import Book, Member, Transaction

@app.route('/')
def index():
    return render_template('index.html')

# Book CRUD
@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        stock = request.form['stock']
        book = Book(name=name, author=author, stock=stock)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('books'))

    books = Book.query.all()
    return render_template('books.html', books=books)

# Member CRUD
@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        name = request.form['name']
        member = Member(name=name)
        db.session.add(member)
        db.session.commit()
        flash('Member added successfully!')
        return redirect(url_for('members'))

    members = Member.query.all()
    return render_template('members.html', members=members)

# Transactions (Issue and Return)
@app.route('/issue', methods=['POST'])
def issue_book():
    member_id = request.form['member_id']
    book_id = request.form['book_id']
    transaction = Transaction(member_id=member_id, book_id=book_id, issue_date=datetime.utcnow())
    db.session.add(transaction)
    db.session.commit()
    flash('Book issued successfully!')
    return redirect(url_for('transactions'))

@app.route('/return', methods=['POST'])
def return_book():
    transaction_id = request.form['transaction_id']
    transaction = Transaction.query.get(transaction_id)
    transaction.return_date = datetime.utcnow()
    db.session.commit()
    flash('Book returned successfully!')
    return redirect(url_for('transactions'))

@app.route('/transactions')
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
