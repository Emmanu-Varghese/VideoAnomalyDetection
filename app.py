from flask import Flask, render_template
from flask import request
import Capture
import Anomaly

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/train",methods=['POST','GET'])
def train_proc():
	if request.method == 'POST':
	    Capture.capture_run(request.form['video_select_train'])
	    return render_template('index.html')
	else:
		return render_template('index.html')

@app.route("/test",methods=['POST','GET'])
def anomaly_proc():
	if request.method == 'POST':
	    Anomaly.anomaly_run(request.form['video_select'],request.form['thresh_select'],request.form['dur_select'])
	    print "Working"
	    return render_template('index.html')
	else:
		return render_template('index.html')

@app.route("/gallery",methods=['POST','GET'])
def show_image():
		return render_template('gallery.html')
if __name__ == "__main__":
    app.run()