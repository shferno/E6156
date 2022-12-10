from flask import Flask, Response, request, render_template
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from circuits_resource import F1
from flask_cors import CORS


# Create the Flask application object.
app = Flask(__name__, template_folder = "/Users/sfy/Desktop/F1/Project/template")
CORS(app)
@app.route('/')
def Home():
    return render_template('../../front-end/template/Home.html')

@app.route("/f1_circuits/add/")
def ad():
    return render_template('../../front-end/template/add.html')

@app.route("/f1/circuits_name", methods = ['GET'])
def circuits_name():
    name = F1.get_circuits_name()
    if name:
        rsp = Response(json.dumps(name), status=200, content_type="application/json")
    else:
        rsp = Response(json.dumps(name), status=404, content_type="text/plain")
    return rsp

# only add name in circuits
@app.route("/f1_circuits/add/", methods = ['POST'])
def add_circuits():
    id = request.form.get('id')
    Ref = request.form.get('circuitRef')
    name = request.form.get('name')
    loc = request.form.get('location')
    country = request.form.get('country')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    alt = request.form.get('alt')
    url = request.form.get('url')
    res = F1.append_new_circuits_name(id, Ref, name, loc, country, lat, lng, alt, url)
    if res:
        return '<script> alert("Fail to add data");location.href = "/";</script>'
    else:
        return '<script> alert("Success");location.hred = "/";</script>'


@app.route('/f1_circuits/update')
def update():
    return render_template('PUT.html')
@app.route('/f1_circuits/update/', methods = ['PUT'])
def update_circuits():
    id = request.form.get('id')
    name = request.form.get('name')
    res = F1.update_circuits(id, name)
    if res:
        return '<script> alert("Fail to update data");location.href = "/";</script>'
    else:
        return '<script> alert("Success");location.hred = "/";</script>'



# @app.post("/f1/add_circuits_name")
# def add_circuits_name():








@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/students/<uni>", methods=["GET"])
def get_student_by_uni(uni):

    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

