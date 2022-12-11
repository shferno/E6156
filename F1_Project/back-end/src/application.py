from flask import Flask, Response, request, render_template
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from circuits_resource import F1
from columbia_student_resource import ColumbiaStudentResource as CSR
from flask_cors import CORS
import re


# Create the Flask application object.
app = Flask(__name__, template_folder = "/Users/sfy/Desktop/F1/Project/template")
CORS(app)
@app.route('/f1_circuits')
def Home():
    return render_template('./template/Home.html')

@app.route("/f1_circuits/add/")
def ad():
    return render_template('./template/add.html')

@app.route("/f1_circuits/circuits_name", methods = ['GET'])
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

# jump to a new page to fill all the required information
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
        return '<script> alert("Success");location.href = "/";</script>'


#
# @app.route("/students/<uni>", methods=["GET"])
# def get_student_by_uni(uni):
#
#     result = ColumbiaStudentResource.get_by_key(uni)
#
#     if result:
#         rsp = Response(json.dumps(result), status=200, content_type="application.json")
#     else:
#         rsp = Response("NOT FOUND", status=404, content_type="text/plain")
#
#     return rsp


# students will jump to the studentHome page
@app.route('/students')
def student_Home():
    return render_template("studentHome.html")

# use firstname
@app.route("/students/fn/<path:first_name>", methods = ["GET"])
def get_student_by_firstname(first_name):
    res = CSR.get_by_firstname(first_name)
    if res:
        rsp = Response(json.dumps(res), status = 200, content_type = "application.json")
    else:
        rsp = Response(json.dumps(res), status = 404, content_type = "text_plain")
    return rsp

# use firstname and address
@app.route("/students/fn/<first_name>/ad/<address>")
def get_student_by_info(first_name, address):
    if address == 'address':
        res = CSR.get_address_by_first_name(first_name)
        if res:
            rsp = Response(json.dumps(res), status=200, content_type="application.json")
        else:
            rsp = Response(json.dumps(res), status=404, content_type="text_plain")
        return rsp
    else:
        if re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", address):
            res = CSR.get_info_by_firstname_address(first_name, address)
            if res:
                rsp = Response(json.dumps(res), status=200, content_type="application.json")
            else:
                rsp = Response(json.dumps(res), status=404, content_type="text_plain")
            return rsp
        else:
            return "<script>alert('wrong email address input');location.href='/';</script>"

        
# use firstname and lastname
@app.route("/students/fn/<first_name>/ln/<last_name>")
def get_student_by_firstname_lastname(first_name, last_name):
    res = CSR.get_info_by_firstname_lastname(first_name, last_name)
    if res:
        rsp = Response(json.dumps(res), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(res), status=404, content_type="text_plain")
    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

