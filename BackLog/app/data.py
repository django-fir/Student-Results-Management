import os
import ast
from .models import *
from datetime import datetime as dt


def get_ride_none(d):
    f = filter(lambda x: True if x[1] else False, d.items())
    return dict(f)


def crate_student():
    files = os.walk(r"C:/Users/Govardhan/Desktop/info/EC/")
    for d, s, f in files:
        for i in f:
            if i.endswith(".py"):
                filer = open(fr"{d}/{i}", 'r')
               # filew = open(fr"{d.replace('results','results1')}/{i}", 'w')
               # filew.write(f"data = {filer.read()}")
               # filew.close()
               # filer.close()
                try:

                    data_list = ast.literal_eval(filer.read())
                    if type(data_list) == 'str':
                        continue
                    data_list = get_ride_none(data_list)

                    name = data_list.get('name', "Unknown")
                    usn = data_list.get('usn')
                    section = data_list.get('section', "A")
                    phone_no = data_list.get('mobile', "0000000000")
                    date_of_birth = dt.strptime(data_list.get(
                        'dateOfBirth', "26 Jan 2001"), "%d %b %Y").strftime("%Y-%m-%d")
                    email = data_list.get('email', "ex@mail.com")
                    father_name = data_list.get('fatherName', "")
                    father_no = data_list.get('fatherMobile', "0000000000")
                    gender = data_list.get('gender', "")
                    idd = data_list.get('id', "")
                    address = data_list.get(
                        'permanentAddress')
                    if address:
                        address = address.get('area', 'Leniyaka')
                    else:
                        address = "Leniyaka"

                    stu = Student.objects.get(usn=usn)
                    stu.section = section
                    stu.address = address
                    stu.phone_no = phone_no
                    stu.date_of_birth = date_of_birth
                    stu.father_name = father_name
                    stu.father_no = father_no
                    stu.gender = gender
                    stu.idd = idd
                    stu.email = email
                    stu.save()
                    if data_list.get('education'):
                        for p in data_list['education']:
                            e = get_ride_none(p)
                            name_e = e.get('qualification', 'Gess')
                            if name_e == 'Gess':
                                name_e = e.get('board', "Gess")
                            obtained_marks = e.get('obtainedMarks', 0)
                            percentage = e.get(
                                'percentageScoreForPlacement', 0)
                            total_marks = e.get('totalMarks', 100)
                            passing_month = e.get('monthOfPassing', '')
                            passing_year = str(passing_month) + \
                                str(e.get('yearOfPassing', ''))
                            collage = e.get("institute", '')
                            Pre_Records.objects.get_or_create(student=stu, name=name_e, obtained_marks=obtained_marks,
                                                              percentage=percentage, collage=collage, total_marks=total_marks, passing_month=passing_year)

                except Exception as er:
                    print(f" : Error :{er}")
                finally:
                    filer.close()
                    print(i)
