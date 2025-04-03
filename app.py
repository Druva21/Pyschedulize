# app.py
from flask import Flask, render_template,request
import random
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def schedule(i):
    temp=[[' ' for i in range(8)] for x in range(5)]
    if i%2==0:
        for x in range(5):
            temp[x][0]='leisuree'
        for x in range(1,4):
            temp[-1][-1*x]='leisuree'
        pass
    else:
        for x in range(5):
            temp[x][-1]='leisuree'
        for x in range(1,5):
            temp[-1][-1*x]='leisuree'
        pass
    return temp

def addCommon(base,time,lis):
    #print(lis)
    for day in range(len(time)):
        for hour in range(len(time[0])):
            if base[day][hour] in lis:
                time[day][hour]=base[day][hour]
                #print(base[day][hour],time[day][hour],'end',end='  ')
    #pprint(base)
    #pprint(time)
    return time
    pass

def findLeisure(credits):
    lis=list()
    for dictionary in credits:
        sum=0
        for values in dictionary.values():
            sum+=values
        lis.append(sum)
        dictionary['leisure']=32-sum
    return credits

def addLeisure(teachers):
    for year in teachers:
        for batch in year:
            batch['leisure']='none'
    return teachers

def checkSameTeacher(teachers,allTimeTables,x,y,classes,pos,batches,day,hour):
    period=classes[pos]
    if period=='leisure':
        return False
    #print(x,y,'error')
    lecturer=teachers[x][y][period]
    for year in range(x+1):
        for batch in range(batches[year]):
            #print(day,hour,'index')
            #print('start')
            #pprint(allTimeTables)
            #pprint(allTimeTables[year][batch])
            #print('done')
            att=allTimeTables[year][batch][day][hour]
            if hour!=0:
                ter=allTimeTables[year][batch][day][hour-1]
            if att!=' 'and att!='leisuree':
                if teachers[year][batch][att]==lecturer:
                    #print('returned true')
                    return True
            if hour!=0:
                if ter!=' ' and ter!='leisuree':
                    if teachers[year][batch][ter]==lecturer:
                        #print('returned true')
                        return True
    #print('returned false')
    return False
    pass

def finishLeisure(time,classes):
    #print('started')
    for x in range(len(time)):
        for y in range(len(time[0])):
            if time[x][y]==' ':
                if len(classes)!=0:
                    pos=random.randint(0,len(classes)-1)
                    time[x][y]=classes[pos]
                    classes.pop(pos)
    #print('finish leisure completed')
    return time
    pass

def fixError(time,classes,pos,teachers,allTimeTables,batches,x,y,day,hour):
    for fix1 in range(len(time)):
        for fix2 in range(len(time[0])):
            if time[fix1][fix2]=='leisure':
                if checkSameTeacher(teachers,allTimeTables,x,y,classes,pos,batches,fix1,fix2):
                    time[fix1][fix2]=classes[pos]
                    time[day][hour]='leisure'
                    return time
    print('Try Again!!!',classes[pos])
    return time
    pass

def assignValues(credits,teachers,x,y,allTimeTables,time,batches,commonCredits):
    classes=list()
    if y!=0:
        for keys in credits[x]:
            if keys not in commonCredits[x]:
                for z in range(credits[x][keys]):
                    classes.append(keys)
    else:
        for keys in credits[x]:
            for z in range(credits[x][keys]):
                classes.append(keys)
    #print(classes)
    random.shuffle(classes)
    for day in range(len(time)):
        #print('1111')
        for hour in range(len(time[0])):
            #print('2222')
            if len(classes)!=0:
                if time[day][hour]==' ':
                    pos=random.randint(0,len(classes)-1)
                    # zzzz=0
                    # while classes[pos]=='leisure':
                    #     zzzz+=1
                    #     if zzzz>10000:
                    #         break
                    #     pos=random.randint(0,len(classes)-1)
                    count=0
                    #print('while')
                    while checkSameTeacher(teachers,allTimeTables,x,y,classes,pos,batches,day,hour):
                        pos=random.randint(0,len(classes)-1)
                        count+=1
                        #print(count)
                        if count>100000:
                            #print('fixerror')
                            time=fixError(time,classes,pos,teachers,allTimeTables,batches,x,y,day,hour)
                            #print('fixerror2')
                            break
                            #time[day][hour]=time[day][hour]
                            #print('No possible timetable with the given information!!.Try Again!!!!!!')
                            #print(time)
                            #print(classes[pos])
                            #exit(0)
                    #print('executed')
                    if count<100000:
                        time[day][hour]=classes[pos]
                        classes.pop(pos)
                    #print('decremented')
            else:
                break
    #print('calling')
    #print('timetable in assignValues: ')
    #pprint(time)
    time=finishLeisure(time,classes)
    #print('assigned')
    return time
    pass

@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    #try:
        # Run your Python script here
        years = request.form['years']
        batches = request.form['batches']
        credits = request.form['credits']
        commonCredits=request.form['commonCredits']
        teachers=request.form['teachers']
        years=eval(years)
        batches=eval(batches)
        credits=eval(credits)
        commonCredits=eval(commonCredits)
        teachers=eval(teachers)
        # print(type(years),':',years)
        # print(type(batches),':',batches)
        # print(type(credits),':',credits)
        # print(type(commonCourses),':',commonCourses)
        # print(type(teachers),':',teachers)
        credits=findLeisure(credits)
        #print(credits)
        teachers=addLeisure(teachers)
        timeTable=[[' ' for i in range(8)] for x in range(5)]
        #print(timeTable)
        timeTable1=schedule(1)
        timeTable2=schedule(2)
        allTimeTables=[[timeTable for x in range(batches[y])] for y in range(years)]
        #print(allTimeTables[0][0])
        classes=list()
        for keys in credits[0]:
            for y in range(credits[0][keys]):
                classes.append(keys)
        random.shuffle(classes)
        time=schedule(1)
        for day in range(len(time)):
            for hour in range(len(time[0])):
                if len(classes)!=0 and time[day][hour]==' ':
                    pos=random.randint(0,len(classes)-1)
                    time[day][hour]=classes[pos]
                    classes.pop(pos)
        allTimeTables[0][0]=time
        #print(allTimeTables[0][0])
        for x in range(years):
            for y in range(batches[x]):
                time=schedule((x+1))
                if y!=0:
                    time=addCommon(allTimeTables[x][0],time,commonCredits[x])
                #print(x,y,'base')
                time=assignValues(credits,teachers,x,y,allTimeTables,time,batches,commonCredits)
                allTimeTables[x][y]=time
        #pprint(allTimeTables)
        for x in allTimeTables:
            for y in x:
                print('Time Table: ')
                for day in y:
                    print(day)
        result = "Timetable generated successfully!"
        return render_template('result.html', console_values=allTimeTables)
        #return render_template('result.html', result=result)
        # except Exception as e:
        #     return ('error processing form data. error is'+str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
