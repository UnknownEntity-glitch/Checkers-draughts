from growler import App, static, render_template

app = App(__name__)
app.use(static.StaticFileMiddleware("static"))

@app.get("/")
def index(req, res):
    return render_template("index.html")

if __name__ == "__main__":
    app.run("localhost", 8000)
