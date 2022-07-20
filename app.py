from turtle import title
from models import (Base, session, Book, engine)
import datetime
import csv


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
    # print(split_date)
    month = int(months.index(split_date[0]) + 1)
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_price(price_str):
    price_float = float(price_str)
    # return '${:,.2f}'.format(price_float)
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
    # app()
    add_csv()
    # print(clean_date('January 1, 2019'))
    # print(clean_price('28.84'))

    for book in session.query(Book).all():
        print(book)
