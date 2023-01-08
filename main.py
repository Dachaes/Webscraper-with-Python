from requests import get
from bs4 import BeautifulSoup
from extractors.remoteok import extract_remoteok_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file
from flask import Flask, render_template, request, redirect, send_file

app = Flask("JobScraper")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword is None or keyword == "":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        remoteok = extract_remoteok_jobs(keyword)
        weworkremotely = extract_wwr_jobs(keyword)
        jobs = remoteok + weworkremotely
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
