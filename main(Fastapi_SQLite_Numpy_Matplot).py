from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="key123")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

con = sqlite3.connect("fit.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    steps INTEGER,
    cal INTEGER,
    sleep REAL,
    weight REAL
)
""")
con.commit()
con.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index1.html", {"request": request})


@app.post("/start", response_class=HTMLResponse)
async def start(request: Request, user: str = Form(...), days: int = Form(...)):
    request.session.clear()
    request.session["user"] = user
    request.session["days"] = days
    request.session["day"] = 1
    request.session["list"] = []
    return templates.TemplateResponse("day1.html", {
        "request": request,
        "day": 1,
        "tot": days,
        "user": user
    })


@app.post("/save", response_class=HTMLResponse)
async def save(request: Request,
               steps: int = Form(...),
               cal: int = Form(...),
               sleep: float = Form(...),
               weight: float = Form(...)):

    user = request.session.get("user")
    tot = request.session.get("days")
    day = request.session.get("day")
    lst = request.session.get("list", [])

    lst.append({"steps": steps, "cal": cal, "sleep": sleep, "weight": weight})
    request.session["list"] = lst
    request.session["day"] = day + 1

    con = sqlite3.connect("fit.db")
    cur = con.cursor()
    cur.execute("INSERT INTO data (user, steps, cal, sleep, weight) VALUES (?, ?, ?, ?, ?)",
                (user, steps, cal, sleep, weight))
    con.commit()
    con.close()

    if day >= tot:
        df = pd.DataFrame(lst)
        a = df["steps"].mean()
        b = df["cal"].mean()
        c = df["sleep"].mean()
        d = df["weight"].mean()

        plt.plot(df["steps"])
        plt.plot(df["cal"])
        plt.plot(df["sleep"])
        plt.xlabel("Day")
        plt.ylabel("Values")
        plt.title("Report")
        p = "static/img.png"
        plt.savefig(p)
        plt.close()

        return templates.TemplateResponse("result1.html", {
            "request": request,
            "user": user,
            "a": round(a, 2),
            "b": round(b, 2),
            "c": round(c, 2),
            "d": round(d, 2),
            "img": "/" + p
        })

    return templates.TemplateResponse("day1.html", {
        "request": request,
        "day": day + 1,
        "tot": tot,
        "user": user
    })
