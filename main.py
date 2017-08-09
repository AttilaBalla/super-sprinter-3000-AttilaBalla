from flask import Flask, render_template, redirect, request, session
import csv

app = Flask(__name__)
app.secret_key = 'ITSSOSECRETDONTTELLANYONE'


def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string


def savetocsv(dictionary):
    FORM_ITEMS = ['title', 'userstory', 'acceptance', 'status']  # sets the order of saving items
    output = []
    for item in FORM_ITEMS:
        if(item in dictionary.keys()):
            output.append(dictionary[item])
        else:
            return False

    writer = csv.writer(open('storydata.csv', 'w'))
    writer.writerow(output)
    return True


@app.route('/')
def route_index():
    return render_template('list.html')


@app.route('/story')
def route_edit():
    return render_template('form.html')


@app.route('/save-story', methods=['POST'])
def route_save():
    result = {}
    print('POST request received!')
    formdata = request.form

    for item in formdata.items():
        result[item[0]] = item[1]

    if(savetocsv(result)):
        print('Data saved successfully!')
    else:
        print('An error occured when saving the data!')
    return redirect('/story')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
