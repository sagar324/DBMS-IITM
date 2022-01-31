import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="academic_insti"
)

mycursor = mydb.cursor()


def checkcourse(c_id):
  stmt = "Select c.cname from course c where c.courseId = '"+c_id+"'"
  
  mycursor.execute(stmt)
  myresult = mycursor.fetchall()

  if len(myresult) == 0:
    return False

  return True

def checkstudent(roll):
  stmt = "Select s.name from student s where s.rollNo = '"+roll+"'"

  mycursor.execute(stmt)
  myresult = mycursor.fetchall()
  
  if len(myresult) == 0:
    return False

  return True


def add_fun(D_id,C_id,T_id,room):
  #D_id = input("Enter Department id: ")
  #C_id = input("Enter Course id: ")
  #T_id = input("Enter teacher id: ")
  #room = input("Enter room number: ")

  mycursor.execute("SELECT courseId FROM course")
  courseIds = mycursor.fetchall()
  if C_id  in [str(x[0]) for x in courseIds] :
    print("Course Id already exists.")
    return

  mycursor.execute("SELECT deptId FROM department")
  deptIds = mycursor.fetchall()
  if D_id not in [str(x[0]) for x in deptIds]:
    print("Invalid Department id.")
    return

  mycursor.execute("SELECT empId FROM professor where deptNo = " + str(D_id))
  empIds = mycursor.fetchall()
  if T_id not in [str(x[0]) for x in empIds]:
    print("Teacher not in the department or teacher doesn't exist.")
    return

  query1 = f"INSERT into course(courseId, deptNo) values (\'{C_id}\', \'{D_id}\')"
  query2 = f"INSERT into teaching(empId, courseId, sem, year, classRoom) values (\'{T_id}\', \'{C_id}\', \'Even\', 2006, \'{room}\')"
  mycursor.execute(query1)
  mycursor.execute(query2)
  mydb.commit()
  print("Course added to the database successfully")

def f_enroll(roll,c_id):
  
  if checkstudent(roll) == False :
    print("student doesnt exist")
    return
  if checkcourse(c_id) == False :
    print("Course doesnt exist")
    return

  stmt = "select p.preReqCourse from prerequisite p , enrollment e where p.courseId = '"+c_id+"' and e.courseId = p.preReqCourse and e.rollNo = '"+roll+"' and (e.grade = 'S' OR e.grade = 'A' OR e.grade = 'B' OR e.grade = 'C' OR e.grade = 'D' OR e.grade = 'E') AND (e.year<2006 OR (e.year = 2006 AND e.sem = 'odd'))"
  mycursor.execute(stmt)
  myresult1 = mycursor.fetchall()

  stmt = "select p.preReqCourse from prerequisite p where p.courseId = '"+c_id+"'"

  mycursor.execute(stmt)
  myresult2 = mycursor.fetchall()

  if len(set(myresult1)) != len(set(myresult2)):
    print( str(len(set(myresult2)) - len(set(myresult1))) + " prerequisites not passed")
    return

  stmt = "INSERT into enrollment values ('"+roll+"','"+c_id+"', 'even', '2006', 'N')"
  mycursor.execute(stmt)
  mydb.commit()

  print("Enrollment added")
  
  return


#main
itrr=0
while 1:
  commandline = str(input())
  commandlist = commandline.split()
  command = commandlist[0]
  if command == "Addition":
    D_id = (commandlist[1])
    C_id = (commandlist[2])
    T_id = (commandlist[3])
    room = commandlist[4]
    #perform department_id update on courses table.
    
    add_fun(D_id,C_id,T_id,room)
    #change room number in teaching table

    
  elif command == "Enrollment":
    roll = (commandlist[1])
    C_id = (commandlist[2])

    f_enroll(roll,C_id)

    # select prereq list, check number of 'Pass's ,next command.
    
    # else insert into enrollment table

  else :
    print("Invalid command at line"+str(itrr+1))
  itrr = itrr + 1
#syntax
#mycursor.execute(sql,val)
#mydb.commit()
