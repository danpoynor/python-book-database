from calendar import c
from turtle import title
from models import (Base, session, Book, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
            \nProgramming Books
            \r1. Add a book
            \r2. List all books
            \r3. Search for a book
            \r4. Book Analysis
            \r5. Exit
            ''')
        choice = input("What would you like to do? ")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above.
                \rA number between 1 and 5.
                \rPress enter to try again.
                ''')


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
    except ValueError:
        input('''
              \n***** DATE ERROR *****
              \rThe date format should include a valid month, day, and year from the past.
              \rEx: January 13, 2003
              \rPress enter to try again.
              \r**********************
              ''')
        return  # Same as return None
    else:
        return datetime.date(year, month, day)


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
              \n***** PRICE ERROR *****
              \rThe price format should be a number without a currency symbol.
              \rEx: 12.99
              \rPress enter to try again.
              \r***********************
              ''')
        return
    else:
        return int(price_float * 100)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter_by(
                title=row[0]).one_or_none()
            if book_in_db is None:
                new_book = Book(
                    title=row[0],
                    author=row[1],
                    publish_date=clean_date(row[2]),
                    price=clean_price(row[3]))
                session.add(new_book)
        session.commit()


def add_book():
    title = input('Title: ')
    author = input('Author: ')
    date_error = True
    while date_error:
        date = input('Published (Ex: October 25, 2017): ')
        date_cleaned = clean_date(date)
        if type(date_cleaned) == datetime.date:
            date_error = False
    price_error = True
    while price_error:
        price = input('Price: (Ex: 12.99): ')
        price_cleaned = clean_price(price)
        if type(price_cleaned) == int:
            price_error = False
    new_book = Book(
        title=title,
        author=author,
        publish_date=date_cleaned,
        price=price_cleaned)
    session.add(new_book)
    session.commit()
    print(f'\n{title} by {author} added to the database.')
    time.sleep(1.5)

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            search_books()
        elif choice == '4':
            book_analysis()
        else:
            print("\nGoodbye!")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()

    for book in session.query(Book).all():
        print(book)
