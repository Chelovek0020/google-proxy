from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder="templates")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return render_template("index.html", error="Введите поисковый запрос")

    google_url = f"https://www.google.com/search?q={query}"
    response = requests.get(google_url, headers=HEADERS)
    if response.status_code != 200:
        return render_template("index.html", error="Ошибка при получении данных с Google")

    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for g in soup.find_all("div", class_="tF2Cxc"):
        title = g.find("h3").text if g.find("h3") else "Без заголовка"
        link = g.find("a")["href"] if g.find("a") else "#"
        results.append({"title": title, "link": link})

    return render_template("results.html", query=query, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
