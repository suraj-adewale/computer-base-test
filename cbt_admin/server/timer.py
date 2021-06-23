from flask import Flask,request, jsonify
import json,sqlite3,base64, time


def Submit(data):
	conn = sqlite3.connect('server/database/cbt.db')
	conn.row_factory=sqlite3.Row
	cursor=conn.cursor()

	regno=data['id']
	course_code=data['course_code']
	testtype=data['testtype']
	year=data['year']

	cursor.execute('''SELECT count(*), status FROM timer WHERE regno=? AND coursecode=? AND date =? ''',\
			(regno, course_code, year))
	submitted=cursor.fetchone()
	print(submitted[1])
	if submitted[1] == 'submitted':
		return 'submitted'

def StartTime(data):
	starttime = time.time()
	conn = sqlite3.connect('server/database/cbt.db')

	regno=data['id']
	course_code=data['course_code']
	testtype=data['testtype']
	year=data['year']
	
	authorid=data['authorid']

	conn.execute('''UPDATE  timer SET starttime=?,endtime=? WHERE regno=? AND authorid=? AND testtype=? AND coursecode=? AND date=? '''\
                         ,(starttime,starttime,regno,authorid,testtype,course_code,year))
	conn.commit()

def EndTime(data):
	endtime = time.time()
	conn = sqlite3.connect('server/database/cbt.db')

	regno=data['id']
	course_code=data['course_code']
	testtype=data['testtype']
	year=data['year']
	
	authorid=data['authorid']

	conn.execute('''UPDATE  timer SET timeallowed= timeallowed + starttime - ?,endtime=?, status=? WHERE regno=? AND authorid=? AND testtype=? AND coursecode=? AND date=? '''\
                         ,(endtime,endtime,'submitted',regno,authorid,testtype,course_code,year))
	conn.commit()
	
def UserDisconnect(data):
	endtime = time.time()
	conn = sqlite3.connect('server/database/cbt.db')

	regno=data['id']
	course_code=data['course_code']
	testtype=data['testtype']
	year=data['year']
	
	authorid=data['authorid']

	conn.execute('''UPDATE  timer SET timeallowed= timeallowed + starttime - ?,endtime=?, status=? WHERE regno=? AND authorid=? AND testtype=? AND coursecode=? AND date=? '''\
                         ,(endtime,endtime,'disconnect',regno,authorid,testtype,course_code,year))
	conn.commit()

def PostTimer():
	conn = sqlite3.connect('server/database/cbt.db')
	conn.execute('''UPDATE  timer SET timeallowed=? WHERE regno=? AND authorid=? AND testtype=? AND coursecode=? AND date=? '''\
                         ,(timer,regno,authorid,testtype,course_code,year))
	conn.commit()
	if request.form.get('action')=='timer':
		data=(request.form.get('data'))
		datadecoded=base64.b64decode(data)
		data=json.loads(datadecoded.decode("utf-8"))

		regno=data['regno']
		course_code=data['course_code']
		testtype=data['testtype']
		year=data['year']
		timer=data['timer']
		authorid=data['authorid']

		conn.execute('''UPDATE  timer SET timeallowed=? WHERE regno=? AND authorid=? AND testtype=? AND coursecode=? AND date=? '''\
                         ,(timer,regno,authorid,testtype,course_code,year))
		conn.commit()
		return jsonify({'timer_choice':'timer'})

	if request.form.get('action')=='timeup':
		data=(request.form.get('data'))
		datadecoded=base64.b64decode(data)
		data=json.loads(datadecoded.decode("utf-8"))
		regno=data['regno']
		course_code=data['course_code']
		testtype=data['testtype']
		year=data['year']
		timer=data['timer']
		authorid=data['authorid']

		conn.execute('''UPDATE  timer SET timeallowed=?, status=? WHERE regno=? AND authorid=? AND testtype=? AND coursecode=? AND date=? '''\
                         ,(0,'submitted',regno,authorid,testtype,course_code,year))
		conn.commit()
		return jsonify({'timer_choice':'timer'})


