from flask import Flask, render_template

app = Flask(__name)

@app.get('/home')
def home():
  return render_template("index.html")
