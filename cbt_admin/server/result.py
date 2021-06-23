import sqlite3

def Result(action,data):

	if action =='schedule':
		conn = sqlite3.connect('server/database/cbt.db')
		print(3456)
		testtitle=data[0]
		testcode=data[1]
		timetaken=int(data[2])*60
		testtype=data[3]
		category=data[4]
		schedule=data[5]
		instantresult=data[6]
		date=data[7]

		conn.execute(''' INSERT INTO schedule (coursetittle,coursecode,category ,authorid,testtype,connection,timeallowed,scheduletime,instantresult,date) \
			VALUES (?,?,?,?,?,?,?,?,?,?)'''\
			,(testtitle,testcode,category,12345,testtype,'offline',timetaken,schedule,instantresult,date))
		conn.commit()
		return 'success'

	if action == 'SelectCategory':
		conn = sqlite3.connect('server/database/cbt.db')		
		Dic={}
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
		cursor=cursor.execute('''SELECT DISTINCT coursecode,  testtype,  year FROM answers ORDER BY year DESC''')
		result=cursor.fetchall()

		rw=0
		for rows in result:
			List=[]
			List.append(rows['coursecode'])
			List.append(rows['testtype'])
			List.append(rows['year'])
			Dic[rw]=List
			rw+=1
		return {'cat':Dic}


	if action =='CheckResult':
		conn = sqlite3.connect('server/database/cbt.db')
		conn.row_factory=sqlite3.Row
		
		
		coursecode=data[0]
		testtype=data[1]
		year=data[2]
		#print(coursecode,testtype,year)
		
		cursor=conn.cursor()
		cursor=cursor.execute('''SELECT DISTINCT section FROM answers WHERE coursecode=? AND testtype=? AND year=? ORDER BY regno DESC'''\
				,(coursecode,testtype,year))
		sections=cursor.fetchall()
		TotalDic={}
		total=0
		for section in sections:
			cursor=cursor.execute('''SELECT count(marks) AS totalmarks FROM questions WHERE coursecode=? AND type=? AND year=? AND section=?'''\
				,(coursecode,testtype,year,section['section']))
			totalmarks=cursor.fetchone()
			TotalDic[section['section']]=totalmarks[0]
			total+=totalmarks['totalmarks']
		TotalDic['total']=total
		
		cursor=cursor.execute('''SELECT DISTINCT regno FROM answers WHERE coursecode=? AND testtype=? AND year=? ORDER BY regno DESC'''\
			,(coursecode,testtype,year))
		regnos=cursor.fetchall()

		ScoresDic={}
		for regno in regnos:
			
			cursor=cursor.execute('''SELECT DISTINCT section FROM answers WHERE coursecode=? AND testtype=? AND year=? ORDER BY regno DESC'''\
				,(coursecode,testtype,year))
			sections=cursor.fetchall()

			sectionDic={}
			List=[]
			total=0
			for section in sections:
				
				cursor=cursor.execute('''SELECT total(marks) AS score FROM answers INNER JOIN  questions ON answers.answer=questions.answer \
				AND answers.answerid=questions.questionid AND answers.section=questions.section\
					WHERE answers.regno=? AND answers.coursecode=? AND answers.testtype=? AND answers.year=? AND answers.section=? ''',\
					(regno['regno'],coursecode,testtype,year,section['section']))
				scores=cursor.fetchall()
				
				for score in scores:
					marks=round((score['score']/TotalDic['total'])*100)
					sectionDic[section['section']]=marks
					total+=marks
				sectionDic['total']=total		
			List.append(sectionDic)
			List.append(coursecode)
			List.append(testtype)
			List.append(year)
			ScoresDic[regno['regno']]=List

		return {'data':ScoresDic}