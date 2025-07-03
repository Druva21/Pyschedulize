from flask import Flask, render_template, request
import random, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    try:
        years = int(request.form['years'])
        batches = json.loads(request.form['batches'])
        periods = int(request.form['periods'])
        start_times = json.loads(request.form['start_times'])
        credits = json.loads(request.form['credits'])
        commonCredits = json.loads(request.form['commonCredits']) if request.form['commonCredits'] else [[] for _ in range(years)]
        teachers = json.loads(request.form['teachers'])

        def schedule_template():
            return [['-' for _ in range(periods)] for _ in range(5)]

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
            if period == 'leisure': return False
            lecturer = teachers[x][y][period]
            for year in range(x + 1):
                for batch in range(batches[year]):
                    att = allTimeTables[year][batch][day][hour]
                    if att != '-' and att != 'leisure':
                        if teachers[year][batch][att] == lecturer:
                            return True
            return False

        def assignValues(credits, teachers, x, y, allTimeTables, time, batches, commonCredits):
            classes = []
            if y != 0:
                for k in credits[x]:
                    if k not in commonCredits[x]:
                        classes += [k] * credits[x][k]
            else:
                for k in credits[x]:
                    classes += [k] * credits[x][k]
            random.shuffle(classes)
            for day in range(5):
                for hour in range(periods):
                    if classes and time[day][hour] == '-':
                        pos = random.randint(0, len(classes) - 1)
                        count = 0
                        while checkSameTeacher(teachers, allTimeTables, x, y, classes, pos, batches, day, hour):
                            pos = random.randint(0, len(classes) - 1)
                            count += 1
                            if count > 1000: break
                        if count < 1000:
                            time[day][hour] = classes[pos]
                            classes.pop(pos)
            return time

        allTimeTables = [[[['-' for _ in range(periods)] for _ in range(5)] for _ in range(batches[y])] for y in range(years)]
        credits = findLeisure(credits)
        teachers = addLeisure(teachers)

        for x in range(years):
            for y in range(batches[x]):
                time = schedule_template()
                if y != 0:
                    for d in range(5):
                        for p in range(periods):
                            if allTimeTables[x][0][d][p] in commonCredits[x]:
                                time[d][p] = allTimeTables[x][0][d][p]
                time = assignValues(credits, teachers, x, y, allTimeTables, time, batches, commonCredits)
                allTimeTables[x][y] = time

        return render_template('result.html', console_values=allTimeTables, start_times=start_times)

    except Exception as e:
        return f"Error processing form data: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
