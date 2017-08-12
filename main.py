from flask import Flask, render_template, redirect, request, session
import csv

FILEPATH = 'storydata.csv'
FORM_ITEMS = ['title', 'userstory', 'acceptance', 'quantity', 'estimation', 'status']
form_selectkeys = ['planning', 'to-do', 'in-progress', 'review', 'done']

app = Flask(__name__)


def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string


def makeselectblock(selectkeys, selectedoption=None):

    result = []
    for item in selectkeys:
        result.append(('"{}"'.format(item), item))

    if(selectedoption is None):
        return result
    else:
        for index, item in enumerate(result):
            if item[1] == selectedoption:
                result[index] = ('"{}" selected'.format(selectedoption), selectedoption)
                break
        return result


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
    newinput = [str(len(filecontents)+1)]  # this will be the ID

    for item in FORM_ITEMS:
        if(item in dictionary.keys()):
            newinput.append(dictionary[item])
        else:
            return False

    newinput[-1] = newinput[-1].strip('"')
    filecontents.append(newinput)
    writer = csv.writer(open('storydata.csv', 'w'))

    for item in filecontents:
        writer.writerow(item)
    return True


def updatecsv(dictionary):
    filecontents = readfromcsv(FILEPATH)
    updatedinput = [dictionary['id']]
    line_id = int(dictionary['id'])-1

    for item in FORM_ITEMS:
        if(item in dictionary.keys()):
            updatedinput.append(dictionary[item])
        else:
            return False

    updatedinput[-1] = updatedinput[-1].strip('"')
    filecontents[line_id] = updatedinput

    writer = csv.writer(open('storydata.csv', 'w'))

    for item in filecontents:
        writer.writerow(item)
    return True


@app.route('/')
def route_index():
    return render_template('list.html', data=readfromcsv(FILEPATH))


@app.route('/story')
def route_create():
    return render_template('form.html', data=None, selectdata=makeselectblock(form_selectkeys))


@app.route('/story/<story_id>')
def route_edit(story_id):
    data = readfromcsv(FILEPATH)
    try:
        _id = int(story_id)
    except ValueError:
        return render_template('list.html', data=data)

    row_list = data[_id-1]
    selected = row_list[-1]

    return render_template('form.html', data=row_list,
                           selectdata=makeselectblock(form_selectkeys, selected))


@app.route('/edit-story', methods=['POST'])
def route_update():
    result = {}
    print('POST request received!')
    formdata = request.form

    for item in formdata.items():
        result[item[0]] = item[1]

    if(updatecsv(result)):
        print('Data updated successfully!')
    else:
        print('An error occured when updating the data!')
    return redirect('/')


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


@app.route('/delete/<story_id>')
def route_delete(story_id):
    result = {}

    filecontents = readfromcsv(FILEPATH)

    for index, item in enumerate(filecontents):
        if (item[0] == str(story_id)):
            del filecontents[index]
            break

    print('deleted:', filecontents)
    writer = csv.writer(open('storydata.csv', 'w'))

    for item in filecontents:
        writer.writerow(item)

    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
