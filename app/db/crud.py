from .models import Book, Category


def create_category(session, title):
    category = Category(title=title)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def get_category(session, category_id):
    return session.get(Category, category_id)


def get_category_by_title(session, title):
    return session.query(Category).filter(Category.title == title).first()


def get_categories(session):
    return session.query(Category).order_by(Category.id).all()


def update_category(session, category_id, title):
    category = get_category(session, category_id)
    if category is None:
        return None

    category.title = title
    session.commit()
    session.refresh(category)
    return category


def delete_category(session, category_id):
    category = get_category(session, category_id)
    if category is None:
        return False

    session.delete(category)
    session.commit()
    return True


def create_book(session, title, description, price, category_id, url=""):
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def get_book(session, book_id):
    return session.get(Book, book_id)


def get_books(session, category_id=None):
    query = session.query(Book)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    return query.order_by(Book.id).all()


def update_book(session, book_id, **fields):
    book = get_book(session, book_id)
    if book is None:
        return None

    for field, value in fields.items():
        if hasattr(book, field):
            setattr(book, field, value)

    session.commit()
    session.refresh(book)
    return book


def delete_book(session, book_id):
    book = get_book(session, book_id)
    if book is None:
        return False

    session.delete(book)
    session.commit()
    return True
