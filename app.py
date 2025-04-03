from flask import Flask, render_template, request
import random
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def schedule(i):
    temp = [[' ' for _ in range(8)] for _ in range(5)]
    if i % 2 == 0:
        for x in range(5):
            temp[x][0] = 'leisuree'
        for x in range(1, 4):
            temp[-1][-1 * x] = 'leisuree'
    else:
        for x in range(5):
            temp[x][-1] = 'leisuree'
        for x in range(1, 5):
            temp[-1][-1 * x] = 'leisuree'
    return temp

def addCommon(base, time, lis):
    for day in range(len(time)):
        for hour in range(len(time[0])):
            if base[day][hour] in lis:
                time[day][hour] = base[day][hour]
    return time

def findLeisure(dictionary):
    total_sum = sum(dictionary.values())  # Use a different variable name
    leisure_hours = 40 - total_sum  # Adjust according to your logic
    dictionary["Leisure"] = leisure_hours
    return dictionary


def addLeisure(teachers):
    for year in teachers:
        for batch in year:
            batch['leisure'] = 'none'
    return teachers

def checkSameTeacher(teachers, allTimeTables, x, y, classes, pos, batches, day, hour):
    period = classes[pos]
    if period == 'leisure':
        return False
    lecturer = teachers[x][y][period]
    for year in range(x + 1):
        for batch in range(batches[year]):
            att = allTimeTables[year][batch][day][hour]
            if att != ' ' and att != 'leisuree':
                if teachers[year][batch][att] == lecturer:
                    return True
    return False

def finishLeisure(time, classes):
    for x in range(len(time)):
        for y in range(len(time[0])):
            if time[x][y] == ' ' and classes:
                pos = random.randint(0, len(classes) - 1)
                time[x][y] = classes.pop(pos)
    return time

def fixError(time, classes, pos, teachers, allTimeTables, batches, x, y, day, hour):
    for fix1 in range(len(time)):
        for fix2 in range(len(time[0])):
            if time[fix1][fix2] == 'leisure':
                if checkSameTeacher(teachers, allTimeTables, x, y, classes, pos, batches, fix1, fix2):
                    time[fix1][fix2] = classes[pos]
                    time[day][hour] = 'leisure'
                    return time
    print('Try Again!!!', classes[pos])
    return time

def assignValues(credits, teachers, x, y, allTimeTables, time, batches, commonCredits):
    classes = []
    for keys in credits[x]:
        if y == 0 or keys not in commonCredits[x]:
            classes.extend([keys] * credits[x][keys])
    random.shuffle(classes)
    for day in range(len(time)):
        for hour in range(len(time[0])):
            if classes and time[day][hour] == ' ':
                pos = random.randint(0, len(classes) - 1)
                count = 0
                while checkSameTeacher(teachers, allTimeTables, x, y, classes, pos, batches, day, hour):
                    pos = random.randint(0, len(classes) - 1)
                    count += 1
                    if count > 100000:
                        time = fixError(time, classes, pos, teachers, allTimeTables, batches, x, y, day, hour)
                        break
                if count < 100000:
                    time[day][hour] = classes.pop(pos)
    return finishLeisure(time, classes)

@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    years = eval(request.form['years'])
    batches = eval(request.form['batches'])
    credits = eval(request.form['credits'])
    commonCredits = eval(request.form['commonCredits'])
    teachers = eval(request.form['teachers'])
    credits = findLeisure(credits)
    teachers = addLeisure(teachers)
    allTimeTables = [[[[' ' for _ in range(8)] for _ in range(5)] for _ in range(batches[y])] for y in range(years)]
    classes = [key for key in credits[0] for _ in range(credits[0][key])]
    random.shuffle(classes)
    time = schedule(1)
    for day in range(len(time)):
        for hour in range(len(time[0])):
            if classes and time[day][hour] == ' ':
                time[day][hour] = classes.pop(random.randint(0, len(classes) - 1))
    for y in range(batches[0]):
        allTimeTables[0][y] = [row[:] for row in time]
    for x in range(years):
        for y in range(batches[x]):
            time = schedule(x + 1)
            if y != 0:
                time = addCommon(allTimeTables[x][0], time, commonCredits[x])
            time = assignValues(credits, teachers, x, y, allTimeTables, time, batches, commonCredits)
            allTimeTables[x][y] = time
    return render_template('result.html', console_values=allTimeTables)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
