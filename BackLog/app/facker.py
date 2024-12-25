import pickle
import json
import datetime
from faker import Faker
import random as rd
gen = Faker()

# {"usn": "1VI19CS031", "subject": "Database Management System", "exam_type": "IA1",
#     "exam_date": "2022-11-22", "marks": 10, "result": true, "sem": "First(1st)"},


def marks(m):
    if "IA" in m:
        return rd.randint(-1, 30)
    else:
        return rd.randint(-1, 60)


def semister(n):
    return n


def usn(n, no):
    # branch = ["CS", "EC", "IS", "ME", "CI", "EE"]
    string = f"1VI{n}CS{no}"
    return string


def subject():
    with open('subject.dat', "rb") as f1:
        data = pickle.load(f1)
        print("Unpickelled")
    return data


def get_subject(n):
    subjects = subject()
    dlist = subjects.get(str(n))
    dummy = {}
    for k, v in dlist.items():
        if k.startswith("18"):
            dummy[k] = v
    return dummy


mode = ["IA1", "IA2", "IA3", "MAIN"]


def results(marks, mode):
    if "IA" in mode:
        if marks >= 18:
            return "Pass"
        elif marks <= 0:
            return "Absent"
        return "Fail"
    else:
        if marks >= 24:
            return "Pass"
        elif marks <= 0:
            return "Absent"
        return "Fail"


def attendence():
    return rd.randint(60, 100)


def asssinment():
    return rd.randint(1, 10)


def main():
    m = 0
    studentl = []
    for p in range(1, 10):
        y = 2017
        for i in range(18, 22):
            u = f"00{p}" if p <= 9 else f"0{p}"if p <= 99 else f"{p}"
            susn = usn(i, u)
            for sem in range(3, 9):
                if sem % 2 == 1:
                    m = 2
                    y += 1
                else:
                    m = 8
                sub = get_subject(sem)
                for ex in mode:
                    d = rd.randint(1, 10)
                    for sc, sn in sub.items():
                        students = {}
                        date = str(datetime.datetime(y, m, d).date())
                        students["usn"] = susn
                        students["sem"] = sem
                        students["exam_type"] = ex
                        students["subject"] = sc
                        marksg = marks(ex)
                        students["marks"] = marksg
                        students["exam_date"] = date
                        students["result"] = results(marksg, ex)
                        students["attendence"] = attendence()
                        students["asinment"] = asssinment()
                        d += 1
                        studentl.append(students)
                    m += 1
    return studentl


with open("data.txt", "w") as f2:
    f2.write(str(main()))
    print("Done")
