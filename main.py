from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'ITSSOSECRETDONTTELLANYONE'


def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string


@app.route('/')
def route_index():
    return render_template('list.html')


@app.route('/story')
def route_edit():
    return render_template('form.html')


@app.route('/save-story', methods=['POST'])
def route_save():
    print('POST request received!')
    formdata = request.form
    print(formdata)
    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
