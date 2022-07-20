from calendar import c
from distutils.command.clean import clean
from turtle import title
from models import (Base, session, Book, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''\nProgramming Books
            \r1. Add a book
            \r2. List all books
            \r3. Search for a book
            \r4. Book Analysis
            \r5. Exit''')
        choice = input("\nWhat would you like to do? ")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above.
                \rA number between 1 and 5.
                \rPress enter to try again.''')


def submenu():
    while True:
        print('''
            \r1. Edit
            \r2. Delete
            \r3. Return to main menu''')
        choice = input("What would you like to do? ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above.
                \rA number from 1-3.
                \rPress enter to try again.''')


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
              \r**********************''')
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
              \r***********************''')
        return
    else:
        return int(price_float * 100)


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
              \n***** ID ERROR *****
              \rThe id should be a number.
              \rEx: 1
              \rPress enter to try again.
              \r********************''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
              \n***** ID ERROR *****
              \rOptions are: {options}
              \rPress enter to try again.
              \r********************''')
            return


def edit_check(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')

    # Print the current value
    if column_name == 'Price':
        print(f'Current {column_name}: ${current_value/100}')
    elif column_name == 'Published_Date':
        print(f'Current {column_name}: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'Current {column_name}: {current_value}')

    # Prompt for a new value
    if column_name == 'Published_Date' or column_name == 'Price':
        while True:
            if column_name == 'Published_Date':
                changes = input('What would you like to change the date to? ')
                changes_cleaned = clean_date(changes)
                if type(changes_cleaned) == datetime.date:
                    return changes_cleaned  # return automatically stops a while loop
            elif column_name == 'Price':
                changes = input('What would you like to change the price to? ')
                changes_cleaned = clean_price(changes)
                if type(changes_cleaned) == int:
                    return changes_cleaned
    else:
        # Must be either Title or Author
        return input('What would you like to change the value to? ')


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


def list_books():
    for book in session.query(Book).order_by(Book.title):
        print(f'{book.id}: {book.title} by {book.author}')
    input('\nPress enter to return to the main menu.')


def search_books():
    id_options = []
    for book in session.query(Book):
        id_options.append(book.id)

    id_error = True
    while id_error:
        id_choice = input(f'''
                \nId options: {id_options}
                \rPlease choose a book by ID.
                \rBook id: ''')
        id_choice_cleaned = clean_id(id_choice, id_options)
        if type(id_choice_cleaned) == int:
            id_error = False
    the_book = session.query(Book).filter_by(id=id_choice_cleaned).first()
    print(f'''
          \n{the_book.title} by {the_book.author}
          \rPublished: {the_book.publish_date}
          \rPrice: ${the_book.price/100}''')

    submenu_choice = submenu()
    if submenu_choice == '1':
        the_book.title = edit_check('Title', the_book.title)
        the_book.author = edit_check('Author', the_book.author)
        the_book.publish_date = edit_check(
            'Published_Date', the_book.publish_date)
        the_book.price = edit_check('Price', the_book.price)
        session.commit()
        print('\nBook updated!')
        time.sleep(1.5)
    elif submenu_choice == '2':
        session.delete(the_book)
        session.commit()
        print('\nBook deleted!')
        time.sleep(1.5)
    else:
        return


def analyze_books():
    oldest_book = session.query(Book).order_by(Book.publish_date).first()
    newest_book = session.query(Book).order_by(
        Book.publish_date.desc()).first()
    total_books = session.query(Book).count()
    python_books = session.query(Book).filter(
        Book.title.like('%Python%')).count()
    print(f'''
          \n***** ANALYZE BOOKS *****
          \rTotal books: {total_books}
          \rOldest book: {oldest_book.title} by {oldest_book.author} published {oldest_book.publish_date}
          \rNewest book: {newest_book.title} by {newest_book.author} published {newest_book.publish_date}
          \rNumber of Python books: {python_books}
          ''')

    # print('\n***** BOOKS BY AUTHOR *****')
    # for author in session.query(Book.author).distinct():
    #     print(f'{author}')

    print('***** BOOKS ORDERED BY PUBLISHED DATE ASCENDING *****')
    for book in session.query(Book).order_by(Book.publish_date):
        print(
            f'{book.publish_date.strftime("%B %d, %Y")} - {book.title} by {book.author}: ${book.price/100}')

    print('\n***** PYTHON BOOKS *****')
    for book in session.query(Book).filter(Book.title.like('%Python%')):
        print(f'{book.title} by {book.author}')

    print('\n***** BOOKS PRICE GREATER THAN $10 *****')
    for book in session.query(Book).filter(Book.price > 1000):
        print(f'${book.price/100}: {book.title} by {book.author}')

    print('\n***** BOOKS PRICE LESS THAN $10 *****')
    for book in session.query(Book).filter(Book.price < 1000):
        print(f'${book.price/100}: {book.title} by {book.author}')

    print('\n***** BOOKS PUBLISHED AFTER 2015 *****')
    for book in session.query(Book).filter(Book.publish_date > '2015-12-31').order_by(Book.publish_date):
        print(f'{book.publish_date}: {book.title}')

    input('\nPress enter to return to the main menu.')


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
            analyze_books()
        else:
            print("\nGoodbye!")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for book in session.query(Book).all():
    #     print(book)
