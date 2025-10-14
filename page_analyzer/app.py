import os
from dotenv import load_dotenv

from page_analyzer.db_functions import (
    get_all_urls,
    add_url,
    get_url_id_by_name,
    get_url_by_id,
    get_url_details,
    add_url_check
)
from page_analyzer.urls_functions import validate_url, get_page_data

from flask import (
    flash,
    Flask,
    render_template,
    request,
    redirect,
    url_for
)


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
HOME_PAGE = "index.html"


@app.route("/")
def index():
    return render_template(HOME_PAGE)


@app.route("/urls", methods=["GET", "POST"])
def urls():
    if request.method == "POST":
        url = request.form.get("url")
        validate_error = validate_url(url)

        if validate_error:
            flash(validate_error, "error")
            return render_template(HOME_PAGE, url=url), 422

        try:
            existing_url = get_url_id_by_name(url)

            if existing_url:
                flash("Страница уже существует", "info")
                return redirect(url_for("url_detail", url_id=existing_url))

            url_id = add_url(url)
            flash("Страница успешно добавлена", "success")
            return redirect(url_for('url_detail', url_id=url_id))

        except Exception:
            flash("При добавлении URL произошла ошибка", "error")
            return render_template(HOME_PAGE, url=url), 500

    return render_template("urls.html", urls=get_all_urls())


@app.route("/urls/<int:url_id>")
def url_detail(url_id):
    url_data = get_url_by_id(url_id)

    if url_data is None:
        flash("Сайт не найден", "error")
        return redirect(url_for("index")), 404

    checks = get_url_details(url_id)

    return render_template("url_detail.html", url=url_data, checks=checks)


@app.route("/urls/<int:url_id>/checks", methods=["POST"])
def url_checks(url_id):
    url_data = get_url_by_id(url_id)

    if url_data is None:
        flash("Сайт не найден", "error")
        return redirect(url_for("urls")), 404

    try:
        check_data = get_page_data(url_data['name'])

        if check_data['status_code'] == 200:
            add_url_check(url_id, check_data)
            flash("Страница успешно проверена", 'success')

    except Exception:
        flash("Произошла ошибка при проверке", "error")

    return redirect(url_for('url_detail', url_id=url_id))


if __name__ == "__main__":
    app.run(debug=True)
