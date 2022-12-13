from flask import Flask, Response, request, render_template
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from circuits_resource import F1
from columbia_student_resource import ColumbiaStudentResource as CSR
from Authentication import Auth
from flask_cors import CORS
import re


# Create the Flask application object.
#template_folder need to update
app = Flask(__name__, template_folder = "/Users/sfy/Desktop/F1/Project/template")
CORS(app)

#navigate to all the pages
@app.route('/')
def Nav():
    return render_template('./template/Navigation')

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST' and 'USER' in request.form and "PASSWORD" in request.form:
        user = request.form.get('USER')
        pw = request.form.get('PASSWORD')
        res = Auth.login_check(user, pw)
        if res:
            # need change to the Home or other pages
            return '<script> alert("Success");location.hred = "/";</script>'
    # need to reload login
    return render_template('./template/login.html')

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

# create a new circuits
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
        return f'<script> alert("{res}");location.href = "/";</script>'
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
        return f'<script> alert("{res}");location.href = "/";</script>'
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

# redirect to student functions' Homepage
@app.route('/students')
def student_Home():
    return render_template("studentHome.html")

# use firstname to get information
@app.route("/students/fn/<path:first_name>", methods = ["GET"])
def get_student_by_firstname(first_name):
    res = CSR.get_by_firstname(first_name)
    if res:
        rsp = Response(json.dumps(res), status = 200, content_type = "application.json")
    else:
        rsp = Response(json.dumps(res), status = 404, content_type = "text_plain")
    return rsp

# use firstname and email address to get information or only get email
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


# use firstname and lastname to get information
@app.route("/students/fn/<first_name>/ln/<last_name>")
def get_student_by_firstname_lastname(first_name, last_name):
    res = CSR.get_info_by_firstname_lastname(first_name, last_name)
    if res:
        rsp = Response(json.dumps(res), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps(res), status=404, content_type="text_plain")
    return rsp
# post function
# not sure whether we need this
@app.route("/students/add/")
def add_student():
    return render_template('./template/create_students.html')

@app.route("/students/add/", methods = ["POST"])
def add_students():
    student_id = request.form.get('id')
    first_name = request.form.get('fn')
    middle_name = request.form.get('mn')
    last_name = request.form.get('ln')
    email = request.form.get('email')
    school_code = request.form.get('sc')
    res = CSR.append_new_students(student_id, first_name, middle_name, last_name, email, school_code)
    if res:
        return f'<script> alert("{res}");location.href = "/";</script>'
    else:
        return '<script> alert("Success");location.hred = "/";</script>'

# update function
# not sure whether we need this
@app.route('/students/update')
def update_students_page():
    return render_template('PUT.html')

# put function
# according firstname update email address
@app.route('/students/update/', methods = ['PUT'])
def update_students():
    first_name = request.form.get('fn')
    email = request.form.get('email')
    res = CSR.update_students_by_firstname(first_name, email)
    if res:
        return f'<script> alert("{res}");location.href = "/";</script>'
    else:
        return '<script> alert("Success");location.href = "/";</script>'


# delete function
@app.route('/students/delete/fn/<firstname>', methods = ["DELETE"])
def delete_students_by_firstname(firstname):
    res = CSR.delete_students_by_firstname(firstname)
    if res:
        return f'<script> alert("{res}");location.href = "/";</script>'
    else:
        return '<script> alert("Success");location.href = "/";</script>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

