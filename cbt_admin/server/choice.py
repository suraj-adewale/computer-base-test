from flask import Flask,request, jsonify
import json,sqlite3,base64


def PostChoice(message):
	
	#if request.form.get("action")=='checkanswers':
	#conn = sqlite3.connect('server/database/cbt.db')
	#data=(request.form.get('data'))
	if message["action"]=='checkanswers':
		datadecoded=base64.b64decode(message["data"])
		data=json.loads(datadecoded.decode("utf-8"))

		conn = sqlite3.connect('server/database/cbt.db')

		regno=data['regno']
		year=data['year']
		testtype=data['testtype']
		coursecode=data['course_code']
		authorid=data['authorid']
		AnswerSectionDic={}
		conn.row_factory=sqlite3.Row

		cursor=conn.cursor()
		cursor1=cursor.execute('''SELECT DISTINCT section FROM answers WHERE regno=? AND coursecode=? AND testtype=? AND authorid=? AND year=?'''\
			,(regno,coursecode,testtype,authorid,year))
		sections=cursor1.fetchall()

		for section in sections:
			answersDic={}
			cursor2=cursor.execute('''SELECT quesno,choicetype,answer FROM answers  WHERE regno=? AND coursecode=? AND testtype=? AND authorid=? AND year=? AND section=?'''\
	                         ,(regno,coursecode,testtype,authorid,year,section['section']))
			quesno=cursor2.fetchall()
			for quesno_choice in quesno:
				choice=quesno_choice['quesno']
				if quesno_choice['choicetype']=='fg':
					answersDic[choice[0]]=quesno_choice['answer']
				if quesno_choice['choicetype']=='mc':
					answersDic[choice[0]]=(choice[1])
			AnswerSectionDic[section['section']]=answersDic
		return jsonify({'timer_choice':'checkanswers','answers':AnswerSectionDic})

	if message["action"]=='postanswer':
		datadecoded=base64.b64decode(message["data"])
		data=json.loads(datadecoded.decode("utf-8"))

		section=data['section']
		choice=data['choice']
		quesno=data['quesno']
		quesno1=data['quesno_']
		regno=data['regno']
		year=data['year']
		testtype=data['testtype']
		choicetype=data['choicetype']
		coursecode=data['course_code']
		authorid=data['authorid']

		try:
			conn = sqlite3.connect('server/database/cbt.db')
			with conn:
				cursor=conn.cursor()
				cursor.execute('''SELECT count(*) FROM answers  WHERE answerid=? AND regno=? AND coursecode=? AND section=? AND testtype=? AND authorid=? AND year=?'''\
									 ,(quesno,regno,coursecode,section,testtype,authorid,year))
				current_answer=cursor.fetchone()

				if current_answer[0]>0:
					cursor.execute('''UPDATE answers SET answer=? WHERE answerid=?  AND regno=? AND coursecode=? AND section=? AND testtype=? AND authorid=? AND year=?'''\
									 ,(choice,quesno,regno,coursecode,section,testtype,authorid,year))
					print({"choice":choice,"server":200})
					return {"choice":choice,"server":200}
				else:
					if cursor.execute('''INSERT INTO answers (answerid,quesno,choicetype,regno,section, coursecode,answer,testtype,authorid,year ) VALUES(?,?,?,?,?,?,?,?,?,?) '''\
								   ,(quesno,quesno1,choicetype,regno,section,coursecode,choice,testtype,authorid,year)):
						print({"choice":choice,"server":200})
						return {"choice":choice,"server":200}
					else:
						print('{"server":205}')
						return '{"server":205}'
		except sqlite3.Error as e:
			return '{"server":205}'



	