from flask import Flask,request, jsonify
import threading,json,sqlite3,base64,random

def Login():
	conn = sqlite3.connect('server/database/cbt.db')
	data={}
	dataDic={}

	if request.form.get('action')=='login':
		data=(request.form.get('data'))
		datadecoded=base64.b64decode(data)
		data=json.loads(datadecoded.decode("utf-8"))
		regno=data['regno']
		password=data['password']
		conn.row_factory=sqlite3.Row
		cursor=conn.cursor()
	
		cursor.execute('''SELECT count(*), * FROM register WHERE password=? AND regno=? ''',\
			(password,regno))
		current_user=cursor.fetchone()
		
		if current_user[0]>0:
			surname=current_user['surname']
			othername=current_user['othername']
			regno=current_user['regno']
			category=current_user['category']
			phone=current_user['phone']
			email=current_user['email']
			authorid=current_user['authorid']

			dataDic['surname']=surname
			dataDic['othername']=othername
			dataDic['regno']=regno
			dataDic['category']=category
			dataDic['phone']=phone
			dataDic['email']=email
			dataDic['authorid']=authorid
			
			cursor=conn.cursor()
			cursor1=cursor.execute('''SELECT schedule.coursetittle AS tittle,schedule.id AS id,schedule.coursecode AS coursecode,schedule.testtype\
			  AS type, schedule.connection AS connection, schedule.category AS category, schedule.timeallowed AS time1,\
			  schedule.scheduletime AS scheduletime,schedule.authorid AS authorid, schedule.date AS date FROM schedule \
			  WHERE  category=? AND authorid=?''',(category,authorid))
			#current_user=cursor.fetchone()
			current_user=cursor1.fetchall()
			scheduledDic={}
			dateDic={}
			questionsDic={}
			constant=random.randint(1,1000)
			for row in current_user:
				dateDic['id']=row['id']
				dateDic['tittle']=row['tittle']
				dateDic['coursecode']=row['coursecode']
				dateDic['type']=row['type']
				dateDic['authorid']=row['authorid']
				dateDic['connection']=row['connection']
				dateDic['category']=row['category']
				dateDic['scheduletime']=row['scheduletime']
				dateDic['date']=row['date']
				#print((regno,row['coursecode'],row['category'],row['authorid'],row['type'],constant,row['date'],row['time1'],'online'))
				curs=cursor.execute('''SELECT count(*),timeallowed AS time2,constant,status,endtime, starttime FROM timer WHERE regno=? AND category=? ''',(regno,category))
				count=curs.fetchone()
				
				if count[0]==0:
					dateDic['timeallowed']=row['time1']
					dateDic['constant']=constant
					conn.execute('''INSERT INTO timer (regno,coursecode,category, authorid, testtype,constant, date,timeallowed,endtime, starttime,status) VALUES(?,?,?,?,?,?,?,?,?,?,?) '''\
	                         ,(regno,row['coursecode'],row['category'],row['authorid'],row['type'],constant,row['date'],row['time1'],0,0,'online'))
					conn.commit()
				else:	
					#timeDiff = count['endtime'] - count['starttime']
			
					dateDic['timeallowed']=(count['time2'])	
					dateDic['constant']=count['constant']
				
				if count['status']=='':
					return jsonify({'login':22,'reason':'You re on session with system number:{}'.format(34567458778)})
					

				#Questions query starts from here:	
				cursor=conn.cursor()
				cursor2=cursor.execute('''SELECT DISTINCT section FROM questions WHERE  coursecode=? AND authorid=?''',(row['coursecode'],row['authorid']))
				sections=cursor2.fetchall()
				questionpara=['questiontype','choicetype','question','choiceA','choiceB','choiceC','choiceD','choiceE','choiceF','choiceG']
				
				totalques=0
				for section in sections:
					
					cursor=conn.cursor()
					cursor3=cursor.execute('''SELECT * FROM questions WHERE  coursecode=? AND authorid=? AND section=?''',(row['coursecode'],row['authorid'],section['section']))
					questions=cursor3.fetchall()
					
					quesDic={}
					for item in questions:		
						quesList=[]
						for para in questionpara:
							if item[para]=='':
								continue
							quesList.append(item[para])
						quesDic[item['questionid']]=quesList	
						
					questionsDic[section['section']]=quesDic	
					totalques+=len(quesDic)
				
				dateDic['totalques']=totalques
				dateDic['questions']=questionsDic
				


				#Already Answers to the question query start from here:
				AnswerquestionsDic={}
				cursor=conn.cursor()
				cursor1=cursor.execute('''SELECT DISTINCT section FROM answers WHERE regno=? AND coursecode=? AND testtype=? AND authorid=? AND year=?'''\
					,(regno,row['coursecode'],row['type'],row['authorid'],row['date']))
				sections=cursor1.fetchall()

				for section in sections:
					answersDic={}
					cursor2=cursor.execute('''SELECT quesno,choicetype,answer FROM answers  WHERE regno=? AND coursecode=? AND testtype=? AND authorid=? AND year=? AND section=?'''\
			                         ,(regno,row['coursecode'],row['type'],row['authorid'],row['date'],section['section']))
					
					quesno=cursor2.fetchall()
					for quesno_choice in quesno:
						choice=quesno_choice['quesno']
						if quesno_choice['choicetype']=='fg':
							answersDic[choice]=quesno_choice['answer']
						if quesno_choice['choicetype']=='mc':
							answersDic[choice[:-1]]=(choice[-1])
					AnswerquestionsDic[section['section']]=answersDic

				dateDic['answers']=AnswerquestionsDic
				scheduledDic[row['date']]=dateDic

			data['profile']=dataDic
			data['schedule']=scheduledDic
			#data['answers']=AnswerquestionsDic
			#print(data)

			return jsonify({'login':1,'data':data})
		else:
			return jsonify({'login':22,'reason':'In correct login details'})

