import os

from flask import (
    Flask, 
    request,
    render_template
)
from .database import (
    add_url,
    get_all_urls,
    get_url_by_id,
    init_db,
    )
from .urls import validate_url

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template(
        'index.html'
    )
    
    
@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        url = request.form.get("url")

        is_valid, error_message = validate_url(url)
        if not is_valid:
            flash(error_message, "error")
            return render_template("index.html", url=url), 422

        try:
            url_id = add_url(url)
            flash("Success adding URL", "success")
            return redirect(url_for("url", url_id=url_id))
        except Exception as e:
            app.logger.error(f"Error adding URL: {e!s}")
            flash("Error adding UR", "error")
            return render_template("index.html", url=url), 422

    urls_list = get_all_urls()
    return render_template("urls.html", urls=urls_list)


@app.route("/urls/<int:url_id>")
def url_show(url_id):
    url_data = get_url_by_id(url_id)
    if not url_data:
        abort(404)
        
    return render_template("url_show.html", url=url_data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)