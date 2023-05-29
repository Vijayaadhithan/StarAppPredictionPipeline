from workerA import add_nums,get_time, get_model, get_accuracy_best_model, get_best_model_name

from flask import (
   Flask,
   request,
   jsonify,
   Markup,
   render_template,
   send_file
)

#app = Flask(__name__, template_folder='./templates',static_folder='./static')
app = Flask(__name__)

@app.route('/')
def index():
    name = get_best_model_name.delay()
    best_model_name = name.get()
    a = get_accuracy_best_model.delay()
    best_model = a.get()
    b = get_model.delay()
    models = b.get()
    return render_template('index.html',best_model_name=best_model_name, best_model=best_model, models=models)

@app.route('/correlation_matrix')
def correlation_matrix():
    return send_file('correlation_matrix.png', mimetype='image/png')

@app.route('/covariance_matrix')
def covariance_matrix():
    return send_file('covariance_matrix.png', mimetype='image/png')

@app.route('/predicted_vs_actual')
def predicted_vs_actual():
    return send_file('predicted_vs_actual.png', mimetype='image/png')

@app.route("/time", methods=['POST', 'GET'])
def time():
    tmp = get_time.delay()
    time = tmp.get()

    return '<h1>The time of the executing models is {}s</h1>'.format(time)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5100,debug=True)
