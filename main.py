from flask import Flask, render_template, redirect, request, session
import csv

FILEPATH = 'storydata.csv'
app = Flask(__name__)
app.secret_key = 'ITSSOSECRETDONTTELLANYONE'


def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string


def readfromcsv(filepath):
    result = []

    try:
        reader = csv.reader(open(filepath, 'r'))
    except FileNotFoundError:
        return []
    for row in reader:
        result.append(row)

    return result


def savetocsv(dictionary):
    filecontents = readfromcsv(FILEPATH)
    FORM_ITEMS = ['title', 'userstory', 'acceptance', 'quantity', 'estimation', 'status']
    # sets the order of saving items
    newinput = [str(len(filecontents)+1)]  # this will be the ID

    for item in FORM_ITEMS:
        if(item in dictionary.keys()):
            newinput.append(dictionary[item])
        else:
            return False
    filecontents.append(newinput)
    writer = csv.writer(open('storydata.csv', 'w'))

    for item in filecontents:
        writer.writerow(item)
    return True


@app.route('/')
def route_index():
    data = readfromcsv(FILEPATH)
    return render_template('list.html', data=data)


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
    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
