from flask import Flask, render_template, request
import random
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def schedule(i, periods):
    temp = [[' ' for _ in range(periods)] for _ in range(5)]
    if i % 2 == 0:
        for x in range(5):
            temp[x][0] = 'leisuree'
        for x in range(1, min(4, periods)):
            temp[-1][-x] = 'leisuree'
    else:
        for x in range(5):
            temp[x][-1] = 'leisuree'
        for x in range(1, min(5, periods)):
            temp[-1][-x] = 'leisuree'
    return temp

def addCommon(base, time, lis):
    for day in range(len(time)):
        for hour in range(len(time[0])):
            if base[day][hour] in lis:
                time[day][hour] = base[day][hour]
    return time

def findLeisure(credits):
    for dictionary in credits:
        total = sum(dictionary.values())
        dictionary['leisure'] = 32 - total
    return credits

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
            if hour != 0:
                ter = allTimeTables[year][batch][day][hour - 1]
            if att != ' ' and att != 'leisuree' and teachers[year][batch][att] == lecturer:
                return True
            if hour != 0 and ter != ' ' and ter != 'leisuree' and teachers[year][batch][ter] == lecturer:
                return True
    return False

def finishLeisure(time, classes):
    for x in range(len(time)):
        for y in range(len(time[0])):
            if time[x][y] == ' ' and classes:
                pos = random.randint(0, len(classes) - 1)
                time[x][y] = classes[pos]
                classes.pop(pos)
    return time

def fixError(time, classes, pos, teachers, allTimeTables, batches, x, y, day, hour):
    for fix1 in range(len(time)):
        for fix2 in range(len(time[0])):
            if time[fix1][fix2] == 'leisure':
                if checkSameTeacher(teachers, allTimeTables, x, y, classes, pos, batches, fix1, fix2):
                    time[fix1][fix2] = classes[pos]
                    time[day][hour] = 'leisure'
                    return time
    return time

def assignValues(credits, teachers, x, y, allTimeTables, time, batches, commonCredits):
    classes = []
    if y != 0:
        for keys in credits[x]:
            if keys not in commonCredits[x]:
                classes.extend([keys] * credits[x][keys])
    else:
        for keys in credits[x]:
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
                    time[day][hour] = classes[pos]
                    classes.pop(pos)
    time = finishLeisure(time, classes)
    return time

@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    try:
        years = int(request.form['years'])
        batches = json.loads(request.form['batches'])
        credits = json.loads(request.form['credits'])
        commonCredits = json.loads(request.form['commonCredits']) if 'commonCredits' in request.form else [[] for _ in range(years)]
        teachers = json.loads(request.form['teachers'])
        periods_per_day = int(request.form['periods'])
        start_times = json.loads(request.form['start_times'])

        credits = findLeisure(credits)
        teachers = addLeisure(teachers)

        allTimeTables = [[[[' ' for _ in range(periods_per_day)] for _ in range(5)] for _ in range(batches[y])] for y in range(years)]

        for x in range(years):
            for y in range(batches[x]):
                time = schedule(x + 1, periods_per_day)
                if y != 0:
                    time = addCommon(allTimeTables[x][0], time, commonCredits[x])
                time = assignValues(credits, teachers, x, y, allTimeTables, time, batches, commonCredits)
                allTimeTables[x][y] = time

        return render_template('result.html',
                               console_values=allTimeTables,
                               start_times=start_times,
                               periods_per_day=periods_per_day)
    except Exception as e:
        return f"Error processing form data: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
