from website import app

app = app.create_app()
app.run(debug=True)