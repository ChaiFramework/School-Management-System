import sys

#Defining Class School.

class School:
    def __init__(self):
        self.students = []

    #read scores method to load data.
    def read_scores(self,file_name):
        with open(file_name) as f:
            file = [_.strip("\n") for _ in f.readlines()]

        header = file[0].split(' ')

        courses = [Course(CID) for CID in header[1:]]
        rows = [row.split(' ') for row in file[1:]]
        students = [Student(row[0],courses,row[1:]) for row in rows]
        
        for student in students:
            student.calculate_average() 

        self.students = students

    def read_scores_and_courses(self,file_name,course_file):

        with open(course_file) as f:
            file = [_.strip("\n") for _ in f.readlines()]

        courses = []
        for row in file:
            courses.append(Course(row.split()[0],row.split()[1],row.split()[2],row.split()[3]) )

        courses_dict = {}
        for c in courses:
            courses_dict[c.CID] = c

        with open(file_name) as f:
            file = [_.strip("\n") for _ in f.readlines()]
        header = file[0].split(' ')[1:]
        courses = [courses_dict[c] for c in header]
        rows = [row.split(' ') for row in file[1:]]
        students = [Student(row[0],courses,row[1:]) for row in rows]

        self.students = students

        for student in students:
            grades = student.grades
            for index,value in enumerate(grades):
                course = courses[index]
                if value == 888:
                    course.enrolled+=1
                elif value == -1:
                    pass
                else:
                    course.enrolled+=1
                    course.total_score+=value

        for course in courses:
            course.calculate_average()

    def read_scores_and_courses_and_students(self,file_name,course_file,student_file):
        with open(course_file) as f:
            file = [_.strip("\n") for _ in f.readlines()]

        courses = []
        for row in file:
            courses.append(Course(row.split()[0],row.split()[1],row.split()[2],row.split()[3]) )

        courses_dict = {}
        for c in courses:
            courses_dict[c.CID] = c

        with open(student_file) as f:
            details = [_.strip("\n") for _ in f.readlines()]

        student_dict = {}
        for row in details:
            row = row.split()
            student_dict[row[0]] = [row[1],row[2]]

        with open(file_name) as f:
            file = [_.strip("\n") for _ in f.readlines()]

        header = file[0].split(' ')[1:]
        courses = [courses_dict[c] for c in header]
        rows = [row.split(' ') for row in file[1:]]
        students = [Student(row[0],courses,row[1:],*student_dict[row[0]]) for row in rows]
        
        self.students = students
        for student in students:
            student.calculate_GPA()
            student.check_criteria()

    #Function to print best performing student.
    def print_highest_student(self):
        spaces = '      '
        length = 0
        print(spaces,end="")
        for course in self.students[0].courses:
            print('| {} '.format(course.CID),end="")
            length+=1
        print("\n------",end="")
        pattern = '|------' * length
        print(pattern)
        sorted_students = sorted(self.students,key = lambda x:x.average,reverse=True)
        for student in sorted_students:
            print(student.SID+" ",end="")
            for index,course in enumerate(student.courses):
                if student.grades[index] == 888:
                    grade = ' '
                elif student.grades[index] == -1:
                    grade = "--"
                else:
                    grade = student.grades[index]
                print("|"," "*(4-len(str(grade))),grade,"  ",sep="",end="")
            print("")
        print("------"+pattern)
        print("{} students, {} courses, the top student is {}, average {}".format(len(self.students),len(self.students[0].courses),sorted_students[0].SID,int(sorted_students[0].average)))

    #Function to print course report.
    def print_course_report(self):
        courses = sorted(self.students[0].courses,key=lambda x:x.average,reverse=True)
        least = courses[-1]
        print("CID     Name         Pt. Enl. Avg.")
        print("----------------------------------")
        for course in courses:
            if course.credits<9:
                space = " "
            else:
                space = ""
            if 'C' in course.type:
                type = '*'
            else:
                type = '-'
            print("{}  {} {}  {}   {}    {}".format(
            course.CID,type,course.name,space+str(course.credits),course.enrolled,course.average)
            )
        print("----------------------------------")
        print("The worst performing course is {} with an average {}".format(least.name,least.average))
        self.generate_course_report()
        print("course_report.txt generated!")

    #Function to write course report.
    def generate_course_report(self):
        courses = sorted(self.students[0].courses,key=lambda x:x.average,reverse=True)
        with open("course_report.txt","w") as op:
            print("CID     Name         Pt. Enl. Avg.",file=op)
            print("----------------------------------",file=op)
            for course in courses:
                if course.credits<9:
                    space = " "
                else:
                    space = ""
                if 'C' in course.type:
                    type = '*'
                else:
                    type = '-'
                print("{}  {} {}  {}   {}    {}".format(
                course.CID,type,course.name,space+str(course.credits),course.enrolled,course.average),file=op
                )
            print("----------------------------------",file=op)

    #Function to view student report.
    def print_student_report(self):
        print("SID    Name        Mode  Enl.  GPA")
        print("------------------------------------")
        for student in sorted(self.students,key = lambda x:x.GPA,reverse=True):
            criteria = " "
            if not student.criteria:
                criteria = '!'
            print("{}  {} {}   {} {}  {}".format(student.SID,student.name,student.role,student.enrolled,criteria,student.GPA))
        self.generate_student_report()
        print("student_report.txt generated!")

    #Function to write student report.
    def generate_student_report(self):
        with open("student_report.txt","w") as op:
            print("SID    Name        Mode  Enl.  GPA",file=op)
            print("------------------------------------",file=op)
            for student in sorted(self.students,key = lambda x:x.GPA,reverse=True):
                criteria = " "
                if not student.criteria:
                    criteria = '!'
                print("{}  {} {}   {} {}  {}".format(student.SID,student.name,student.role,student.enrolled,criteria,student.GPA),file=op)


#Defining Class Student.

class Student:
    def __init__(self, ID,courses,grades, name = '', role = ''):
        self.SID = ID
        self.courses = courses
        self.grades = list(map(int,grades))
        self.average = 0
        self.GPA = '--'
        self.role = role
        self.name = name + " "*(12-len(name))
        self.criteria = False
        self.enrolled = 0

    #Function to calculate average score.
    def calculate_average(self):
        sum = total = 0
        for grade in self.grades:
            if grade == 888:
                pass
            elif grade == -1:
                pass
            else:
                sum+=grade
                total+=1
        if total!=0:
            self.average = sum/total

    
    #Function to calculate GPA.

    def calculate_GPA(self):
        gpa = total = 0
        for grade in self.grades:
            if grade == -1 or grade == 888:
                pass
            if grade>=80:
                gpa+=4
            elif 70<=grade<=79:
                gpa+=3
            elif 60<=grade<=69:
                gpa+=2
            elif 60<=grade<=69:
                gpa+=1
            total+=1
        if total!=0:
            self.GPA = round(gpa/total,2)

    #Function to check criteria.

    def check_criteria(self):
        count = 0
        for index,course in enumerate(self.courses):
            if self.grades[index]!=-1 and 'C' in course.type:
                count+=1
            if ('C' in course.type or 'E' in course.type) and self.grades[index]!=-1:
                self.enrolled+=1

        if count>=3 and self.role == 'FT':
            self.criteria = True
        if count>=2 and self.role == 'PT':
            self.criteria = True



#Defining Class Course.

class Course:
    def __init__(self, ID, name = '', type = '', credits = 0):
        self.CID = ID
        self.name = name+" " * (11-len(name))
        self._type = type
        self.credits = int(credits)
        self.enrolled = 0
        self.total_score = 0

    @property
    def type(self):
        return self._type

    #function to set type of course.
    def set_type(self,type):
        if 'C' in self.type and 'C' in type:
            self.type = type
        elif 'E' in self.type and 'E' in type:
            self.type = type
        else:
            print("ERROR")

    #Function to calculate average.
    def calculate_average(self):
        if self.enrolled >0 and self.total_score>0:
            self.average = self.total_score//self.enrolled
        else:
            self.average = '--'




#Main to perform operations.

if __name__=='__main__':
    if len(sys.argv) == 2:
        s = School()
        s.read_scores(sys.argv[1])
        s.print_highest_student()
    elif len(sys.argv) == 3:
        s = School()
        s.read_scores_and_courses(sys.argv[1],sys.argv[2])
        s.print_course_report()
    elif len(sys.argv) == 4:
        s = School()
        s.read_scores_and_courses_and_students(sys.argv[1],sys.argv[2],sys.argv[3])
        s.print_student_report()

