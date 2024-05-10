from flask import Blueprint, request, render_template, url_for, make_response
from flask_login import login_required, current_user

from webapp import es
from webapp.models.book_model import Book

search_bp = Blueprint('search', __name__)
MAX_SIZE = 15


@search_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    query = request.form["q"].lower() if request.method == "POST" else request.args["q"].lower()
    if request.method == 'POST':
        response = make_response()
        # Million dollar response
        response.headers['HX-Redirect'] = url_for('search.display_search', query=query)
        return response
        # Default GET behavior: Render a partial for live search
    books = query_book(query)
    return render_template("components/search_response_list.html", books=books)


@search_bp.route('/display', methods=['GET'])
@login_required
def display_search():
    is_logged_in = current_user.is_authenticated
    query = request.args.get('query', '')
    books = query_book(query)
    isbn_list = [b["isbn"] for b in books]
    books = Book.query.filter(Book.isbn.in_(isbn_list)).all()

    return render_template("components/search_response_page.html", books=books, is_logged_in=is_logged_in)


def query_book(title):
    search_query = {
        "bool": {
            "must": [
                {"multi_match": {
                    "query": title,
                    "fields": ["title^3", "author"],  # Boost title field
                    "fuzziness": "AUTO"
                }}
            ]
        }
    }

    # Executing the search query
    resp = es.search(index="books", body={"query": search_query}, size=MAX_SIZE)

    titles = [result['_source']['title'] for result in resp['hits']['hits']]
    doc_ids = [result['_id'] for result in resp['hits']['hits']]
    # Creating a list of dictionaries that include title, isbn, and document id
    books = [{"title": title, "isbn": doc_id} for title, doc_id in zip(titles, doc_ids)]
    return books
