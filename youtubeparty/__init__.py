from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

dumb_db = []

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    dumb_db.append(request.form['youtube-url'])
  return render_template('index.html', queue=dumb_db)

@app.route('/upload-url', methods=['POST'])
def upload_url():
  dumb_db.append(request.form['youtube-url'])
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.debug = True
  app.run()
