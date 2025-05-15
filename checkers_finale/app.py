from growler import App, Response, middleware

app = App('checkers_growler')

@app.use
@middleware
async def logger(req, res, next):
    print(f"{req.method} {req.url}")
    await next()

@app.get("/")
async def index(req, res):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Checkers Game</title>
    </head>
    <body>
        <h1>Checkers Game (Run checkers.py locally to play)</h1>
        <p>This Growler server is just a placeholder for browser access or status display.</p>
    </body>
    </html>
    """
    res.send(Response(html, content_type="text/html"))

if __name__ == "__main__":
    app.create_server(host='127.0.0.1', port=8000).run_forever()
