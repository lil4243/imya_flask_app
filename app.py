from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, session
import os

app = Flask("имя")
app.secret_key = "песок_на_море"  # придумай свой

# Страница с файлами
FOLDER = "files"
# Пароль
PASSWORD = "прелесть"

# Страница входа
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("files"))
        else:
            error = "Неверный пароль"
    return render_template_string(f"""
        <h2>Вход</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Введите пароль">
            <button type="submit">Войти</button>
        </form>
        <p style="color:red;">{error}</p>
    """)

# Страница с файлами
@app.route("/files")
def files():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    files_list = os.listdir(FOLDER)
    html = "<h2>Файлы:</h2><ul>"

    for f in files_list:
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            html += '<li>'
            html += f'<p>{f}</p>'
            html += f'<img src="/file/{f}" width="200">'
            html += '</li>'
        else:
            html += f'<li><a href="/file/{f}">{f}</a></li>'

    html += "</ul>"
    html += '<br><a href="/logout">Выйти</a>'
    return render_template_string(html)

# Открытие файлов
@app.route("/file/<path:filename>")
def get_file(filename):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_from_directory(FOLDER, filename)

# Выход
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)