from .data import crate_student
import plotly.graph_objects as go
import plotly.io as plt_io
import plotly.express as px
import numpy as np
import base64
import dataframe_image as dfi
from django.db.models import Count
import pandas as pd
from django.http import HttpResponse
import requests
import ast
from pprint import pformat
import os
import pickle
import random as rd
# from faker import Faker
import datetime
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.db.models import Q
plt_io.templates.default = 'plotly_dark'

# Create your views here.


def add_students(request):
    crate_student()
    return None


def home(request, key):

    return render(request, "index.html", {"home": True})


def search(request):
    return render(request, "search.html", {"enables": True})


def search_query(request, key):
    studets = []
    stu = Student.objects.filter(
        Q(usn__icontains=key) | Q(name__icontains=key)).values("usn", "name")[:150]
    # print(type(stu))
    for i in stu:
        studets.append(f'{i["usn"]}  {i["name"]}')
    return JsonResponse(studets, safe=False)


def wasup_search(request):
    un = ''
    key = request.GET.get('q')
    branch = request.GET.get('br')
    batch = request.GET.get('ba')
    stu = Student.objects.filter(Q(name__istartswith=key) &
                                 Q(branch=branch) & Q(batch=batch)).values("usn", "name")[:100]
    for i in stu:
        un += f'{i["usn"]} : {i["name"]}\n'
    return JsonResponse(un, safe=False)


def wasup_info(request):
    u = ''
    key = request.GET.get('q')
    menu = request.GET.get('m')
    if menu == 'e':
        edu = Pre_Records.objects.filter(student__usn=key).values()
        for i in edu:
            for k, v in i.items():
                u += f"{k} = {v}\n"
        return JsonResponse(u, safe=False)
    else:
        stu = Student.objects.filter(usn__iexact=key).values()
        for k, v in list(stu)[0].items():
            u += f"{k} = {v}\n"
        return JsonResponse(u, safe=False)


def get_student_details(request, key=None):
    if key:
        details = list(Example.objects.filter(student__usn__icontains=key).values(
            "student__usn", "sem", "exam_type__name", "subject__code", "main_marks", "entry_date", "result", "student__spass", "student__sfail", "ia_marks"))

        # result = (Example.objects.filter(
        #     student__usn__icontains=key).values("result", "sem").annotate(rcount=Count("sem")).values("result", "sem").annotate(resultc=Count("result"))).order_by()
        # print(result)
        return JsonResponse(details, safe=False)
    else:
        data = list(Example.objects.values(
            "student__usn", "sem", "exam_type__name", "subject__code", "obtained_marks", "entry_date", "result", "ia_marks"))
        return JsonResponse(data, safe=False)


# def fackgenerator(request):
    """name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    attendence = models.IntegerField(default=0)
    assinment = models.IntegerField(default=5)
    sem = models.ForeignKey(Sem, on_delete=models.CASCADE)"""

    gen = Faker()

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
        with open(r'C:\Users\Govardhan\BackLog\subject.dat', "rb") as f1:
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

    def internals():
        for i in ["IA1", "IA2", "IA3", "MAIN-1", "MAIN-R", "MAIN-2"]:
            EName.objects.get_or_create(name=i)

    def modes():
        for i in ["IA1", "IA2", "IA3", "MAIN-1", "MAIN-R", "MAIN-2"]:
            min = 0
            max = 0
            sub = EName.objects.get(name=i)
            if "IA" in i:
                min = 18
                max = 30
            else:
                min = 24
                max = 60
            ExamMode.objects.get_or_create(
                name=sub, min_marks=min, max_marks=max)

    def semister():
        for i in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]:
            Sem.objects.get_or_create(name=i)

    def msubjects():
        for i in range(3, 9):
            sem = Sem.objects.get(name__contains=f"{i}")
            # print(sem)
            sub = get_subject(i)
            for c, n in sub.items():
                pp = Subject.objects.get_or_create(
                    sem=sem, code=c, name=n)
                print(pp)

    def mstudent():
        for y in range(17, 22):
            for s in range(1, 9):
                sem = Sem.objects.get(name__contains=f"{s}")
                for sec, uno in [("A", 1), ("B", 51), ("C", 101)]:
                    for no in range(uno, uno+50):
                        u = f"00{no}" if no <= 9 else f"0{no}"if no <= 99 else f"{no}"
                        susn = usn(y+s, u)
                        name = gen.name()
                        Student.objects.get_or_create(
                            name=name, sem=sem, usn=susn, section=sec)

    def exam_detailes():
        """student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    Emode = models.ForeignKey(ExamMode, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    exam_date = models.DateField()
    attendence = models.IntegerField(default=0)
    assinment = models.IntegerField(default=5)
    obtained_marks = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=10, choices=(
        ("Pass", "Pass"), ("Fail", "Fail"), ("Absent", "Absent")), default="Pass", editable=False)"""

        student = Student.objects.all()
        sub = Subject.objects.all()
        emode = ExamMode.objects.all()
        # exam_date = str(datetime.datetime().date())
        attendenc = attendence()
        assinmen = asssinment()
        # obtained_marks = marks(ex)

        for i in student:
            for k in sub.filter(sem=i.sem):
                for j in emode:
                    Exam_Result.objects.get_or_create(student=i, subject=k, Emode=j, exam_date=str(gen.date()), attendence=attendence(),
                                                      assinment=asssinment(),
                                                      obtained_marks=marks(j.name.name))
    # internals()
    # modes()
    # semister()
    # msubjects()
    # mstudent()
    # exam_detailes()

    def pickelload():
        with open(r"C:\Users\Govardhan\BackLog\datap.dat", "rb") as f1:
            text = pickle.load(f1)
        return text

    def adddata():
        list = pickelload()
        sections = ["A", "B", "C"]
        v = 0
        for i in list:
            obj = Student.objects.filter(usn=i["usn"])
            if len(obj) == 0:
                Student.objects.get_or_create(usn=i["usn"], name=gen.name(),
                                              section=sections[int(v % 3)])

            v += 1

    # adddata()

    def exampledata():
        list = pickelload()
        for i in list:
            student = Student.objects.get(usn=i["usn"])
            # print(i["exam_type"])
            exam_type = ExamMode.objects.get(name__name=i["exam_type"])
            subject = Subject.objects.get(code=i['subject'])
            # print(student, exam_type, subject)
            Example.objects.get_or_create(student=student, sem=i["sem"], exam_type=exam_type, subject=subject,
                                          obtained_marks=i["marks"], exam_date=i["exam_date"], attendence=i['attendence'], asinment=i["asinment"])
    exampledata()


def original_data(request):
    files = os.walk(r"C:/Users/Govardhan/Desktop/results/EC/")
    for d, s, f in files:
        for i in f:
            filer = open(fr"{d}/{i}", 'r')
            # filew = open(fr"{d.replace('results','results1')}/{i}", 'w')
            # filew.write(f"data = {filer.read()}")
            # filew.close()
            # filer.close()
            try:
                data_list = ast.literal_eval(filer.read())
            except:
                print("Error")
            for data in data_list:
                name = data['name']
                exam_type = data['resultMonthYear']
                sem = data['semester']
                batch = data['batchYear']
                branch = data['branchCode']
                subjects = data['subjects']
                total_marks = data['total']
                usn = data['usn']
                print(f"{usn} : {name}")
                try:
                    stu = Student.objects.get_or_create(
                        name=name, usn=usn, batch=batch, branch=branch)
                    exam_mode = ExamMode.objects.get_or_create(name=exam_type)
                except Exception as e:
                    print(f"{usn} {e}")
                for e in subjects:
                    try:
                        sub_name = e['subjectName']
                        sub_code = e['subjectCode']
                        ia_marks = e['iaMarks']
                        main_marks = e['eMarks']
                        result = e['result']
                        total = e['total']
                        print("Done")
                        sub_d = Subject.objects.get_or_create(
                            name=sub_name, code=sub_code)
                        exam = Example.objects.get_or_create(student=stu[0], sem=sem, exam_type=exam_mode[0], subject=sub_d[0],
                                                             ia_marks=ia_marks, main_marks=main_marks, total_marks=total, result=result)
                    except:
                        print(f"{usn} : Error")

            filer.close()


def create_record(data):
        list_recors = []
        # print(data_list)
        name = data.get('name',"xyz")
        exam_type = data.get('resultMonthYear',"None")
        sem = data.get('semester',"current")
        batch = data.get('batchYear','None')
        branch = data['branchCode']
        subjects = data['subjects']
        total_marks = data['total']
        usn = data['usn']
        # print(f"{usn} : {name}")
        stu = Student.objects.get_or_create(
            name=name, usn=usn, batch=batch, branch=branch)
        exam_mode = ExamMode.objects.get_or_create(name=exam_type)
        for e in subjects:
            try:
                sub_name = e['subjectName']
                sub_code = e['subjectCode']
                ia_marks = e['iaMarks']
                main_marks = e['eMarks']
                result = e['result']
                total = e['total']
                dic_obj = {
                    "name": name,
                    "branch": branch,
                    "batch": batch,
                    "sem": sem,
                    "exam_type": exam_type,
                    "usn": usn,
                    "sub_name": sub_name,
                    "sub_code": sub_code,
                    "ia_marks": ia_marks,
                    "main_marks": main_marks,
                    "result": result,
                    "total": total,
                }
                # list_recors.append(dic_obj)
                # print("Done")
                sub_d = Subject.objects.get_or_create(
                    name=sub_name, code=sub_code)
                exam = Example.objects.get_or_create(student=stu[0], sem=sem, exam_type=exam_mode[0], subject=sub_d[0],
                                                     ia_marks=ia_marks, main_marks=main_marks, total_marks=total, result=result)
            except Exception as e:
                print(f"{usn} : Error {e}")
            finally:
                print(f"{usn}:{sub_code} Done")
        # return list_recors
headders = {
    "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 11; 2107113SI Build/SKQ1.211006.001)",
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzY2ExYWU0NzNlNzZhYmZhMDdlNDcwNiIsImF2YXRhciI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FFZEZUcDRsUDN2MmxIZ3Z3WUJ0WXlQa0dtNW9rUUh5NDBmLTBXNVVnOTduV2c9czk2LWMiLCJmdWxsTmFtZSI6IkdvdmFyZGhhbiBSZWRkeSIsImVtYWlsIjoiZ292YTk2MzJAZ21haWwuY29tIiwic2NvcGUiOlsidXNlciJdLCJ1c24iOiIxVkkxOUNTMDMxIiwiY2xhc3NJZCI6IjFWSTE5Q1MiLCJjb2xsZWdlSWQiOiIxVkkiLCJ5ZWFyIjoiSSIsImNvbGxlZ2UiOiJWRU1BTkEgSU5TVElUVVRFIE9GIFRFQ0hOT0xPR1kgIiwic2NoZW1lIjoiMjAxOCIsInNlbWVzdGVyIjoiViIsImJyYW5jaCI6IkNTRSIsInR5cGUiOiJzdHVkZW50IiwidmVyaWZpZWQiOmZhbHNlLCJpYXQiOjE3MDQ4NjQ3NzAsImV4cCI6MTcwNTQ2OTU3MH0.Tyfy1hMtRKL2q6sPJ5nMWk9HOAS5BqmueVptBuEGluo"
}

def get_results(request, branch, code, api=False, headders=headders):
    # headders = {
    #   "X-Requested-with":"XMLHttpRequest",
    #   "Accept": "application/json, text/plain, */*",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InNjb3BlIjpbInVzZXIiXSwiZW1haWwiOiJuYW5kYW5AZ21haWwuY29tIn0sImlhdCI6MTU0NzMxODI5N30.ZPO8tf03azhTJ1qmgSVyGV80k9EfomXgGazdLyUC6fw",
    # "Connection": "keep-alive"
    # }
    # file = open("result.txt",'w')
    # branch = "CS"
    # code = 21
    clg = request.GET.get("code", "1VI")
    print(request.GET.get("code"))
    USN = f"{clg}{code}{branch}000"
    tr = 0
    sem = request.GET.get("sem")
    list = []

    for i in range(1, 200):
        leng = len(str(i))
        usn = USN[:-leng]+str(i)
        # file = open(fr"C:\Users\Govardhan\Desktop\results\{branch}\{code}\{usn}.py",'w')
        try:
            url = f"https://api.vtuconnect.in/v2/result/{usn}"
            res = requests.get(url, headers=headders)            

            for i in res.json():
                a = "https://api.vtuconnect.in/v2/result/sem?usn={}&yearmonth={}&sem={}".format(i["usn"],i["resultMonthYear"],i["semester"])
                res_s  = requests.get(a,headers=headders)
                if len(res_s.json()) > 0:
                    cre = create_record(res_s.json())
                    list.extend(cre)
                else:
                    tr += 1
                    print(f"{usn} error")
                    if tr == 10:
                        break
        except Exception as e:
            # file.write(pformat(res.text))
            # print("text")
            print(f"{usn}  error{e} ")

        finally:
            # file.close()
            # print(usn)
            pass
    if api:
        return JsonResponse(list, safe=False)
    return render(request, 'result.html', {"home": True})


def convert_date(data):
    m = data.split('/')
    y = data[-1:-4]
    return m[0]+m[1]+y


def send_data(path):
    excel = open(path, 'rb')
    excel_data = base64.b64encode(excel.read()).decode('utf-8')
    excel.close()
    return excel_data


def send_tel(request, path):
    f = open(path, 'rb')
    return HttpResponse(f.read(), content_type="image/jpeg")


def chat_bot(request):
    usn = request.GET.get('usn')
    sem = request.GET.get('sem', 1)
    menu = request.GET.get('m')
    csv = request.GET.get('csv')
    data_q = Example.objects.filter(student__usn=usn)
    data_m = pd.DataFrame(data_q.values('student__usn', 'student__name', 'sem', 'exam_type_id__name',
                                        'subject__code', 'ia_marks', 'main_marks', 'total_marks', 'result'))
    data_m.set_axis(['usn', 'name', 'sem', 'date', 'subj', 'ia_marks', 'main_marks',
                     'total_marks', 'result'], axis='columns', inplace=True)
    # data.to_csv('studentsa.csv')
    # return None
    if 'ex' == menu:
        final_set = data_m
        if 'csv' == csv:
            return HttpResponse(final_set.to_csv(index=False))
        path = r"C:\Users\Govardhan\BackLog\BackLog\admin-interface\wasup\excel\class\result.xlsx"
        final_set.to_excel(path)
        return JsonResponse(send_data(path), safe=False)

    if 'gp' == menu:
        html = graph_student(data_m, usn)

        html = base64.standard_b64encode(bytes(html, 'utf-8')).decode('utf-8')
        return JsonResponse(html, safe=False)

    data = data_m[data_m['sem'] == f'{sem}']
    if 'gb' == menu:
        # if len(data["name"]) > 1:
        html = result_bar2(data_m, usn, sem)

        html = base64.standard_b64encode(
            bytes(html, 'utf-8')).decode('utf-8')
        return JsonResponse(html, safe=False)

    data['ia_marks'] = data['ia_marks'].astype(str)
    data['main_marks'] = data['main_marks'].astype(str)
    data['total_marks'] = data['total_marks'].astype(str)
    data["IA+MN=TO"] = data["ia_marks"] + ' + ' + \
        data["main_marks"]+' = '+data["total_marks"]

    data = data[['subj', 'IA+MN=TO', 'result']]

    df = data

    def styles(x):
        if x["result"] == "P":
            return [f"color:{'lawngreen'};" for i in x]
        elif x["result"] == "F":
            return [f"color:{'#E32636'};" for i in x]
        else:
            return [f"color:{'#00FFFF'};" for i in x]

    df = df.style.apply(styles, axis=1)\
        .set_properties(**{'background-color': 'black', 'border-color': 'white'})\
        .set_table_styles([{"selector": "th", "props": "color: white;background-color:black;"}])\
        .hide(axis="index")
    df.set_caption(f"{data_q[0].student.name[:15]};  SEM: {sem}")

    dfi.export(
        df, r"C:\Users\Govardhan\BackLog\BackLog\admin-interface\wasup\images\result\styled.png")

    return JsonResponse(send_data(r'C:\Users\Govardhan\BackLog\BackLog\admin-interface\wasup\images\result\styled.png'), safe=False)


def excel_collage(result):
    resulta = result[['usn', 'total_marks', 'name', 'main_marks']].groupby(
        "usn").sum().sort_values(["total_marks", "main_marks"], ascending=False)
    final = resulta.join(
        result[["name", "usn"]].drop_duplicates().set_index('usn')).reset_index()
    final["Rank"] = final.index + 1
    path = r"C:\Users\Govardhan\BackLog\BackLog\admin-interface\wasup\excel\class\result.xlsx"
    final.set_index('usn').to_excel(path)


def excel_subject(data, path):
    res = data.pivot(index="usn", columns="subj", values=["total_marks"])
    res[("total_marks", "total")] = res.sum(axis=1)
    res.style.apply(lambda x: np.where(
        x < 40, 'color:red;', 'color:green')).to_excel(path)


def result_insights(request):
    menu = request.GET.get('m')
    sem = request.GET.get('s')
    branch = request.GET.get('br')
    batch = request.GET.get('bat')
    sub = request.GET.get('sub')
    csv = request.GET.get('csv')
    exam_date = Example.objects.filter(sem=sem, student__usn__regex=f"1VI{batch}{branch}.*").values(
        'exam_type__name').annotate(count=Count("exam_type__name")).order_by('-count')[0]['exam_type__name']

    data_q = Example.objects.filter(
        sem=sem, exam_type__name=exam_date, student__branch=branch)
    if sub:
        data_q = data_q.filter(subject__code=sub)
        print(data_q)

    result = pd.DataFrame(data_q.values('student__usn', 'student__name', 'sem', 'exam_type_id__name',
                                        'subject__code', 'ia_marks', 'main_marks', 'total_marks', 'result'))
    result.set_axis(['usn', 'name', 'sem', 'date', 'subj', 'ia_marks', 'main_marks',
                     'total_marks', 'result'], axis='columns', inplace=True)
    if menu == "c":
        if 'csv' == csv:
            return HttpResponse(result.to_csv(index=False))
        path = r"C:\Users\Govardhan\BackLog\BackLog\admin-interface\wasup\excel\class\result.xlsx"
        excel_collage(result)
        return JsonResponse(send_data(path), safe=False)
    elif menu == "as":
        if 'csv' == csv:
            return HttpResponse(result.to_csv(index=False))
        path = r"C:\Users\Govardhan\BackLog\BackLog\admin-interface\wasup\excel\class\resultas.xlsx"
        excel_subject(result, path)
        return JsonResponse(send_data(path), safe=False)
    elif menu == "gs":
        fig = px.scatter(result, x="ia_marks", y="total_marks", color="result", hover_data=[
                         "usn"], marginal_y="histogram", marginal_x="rug",
                         title=f"{sub}- {sem}th sem")
        html = fig.to_html(include_mathjax="cdn", include_plotlyjs="cdn")
        html = base64.standard_b64encode(
            bytes(html, 'utf-8')).decode('utf-8')
        return JsonResponse(html, safe=False)


"""application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"""


def graph_student(sud, usn):
    sudp = sud[sud["result"] == "P"]["result"].count()
    sudt = sud["subj"].unique().shape[0]
    sudf = sudt-sudp
    stu = Student.objects.get(usn=usn)
    stu.sfail = sudf
    stu.spass = sudp
    stu.save()
    fig = px.sunburst(sud,
                      path=["sem", "subj", "total_marks"],
                      values="total_marks",
                      color="result",
                      color_discrete_map={"P": "darkgreen",
                                          "F": "darkred", "A": "blue"},
                      hover_data=["date"],
                      title=f"USN : {usn} (Pass:{sudp},Fail:{sudf})<br>NAME : {sud['name'][0]}",

                      )
    fig.update_layout(margin=dict(t=35, l=0, r=0, b=0))
    html = fig.to_html(include_mathjax="cdn", include_plotlyjs="cdn")
    # print(html)
    return html


def result_bar(sud3, usn, sem):
    fig = go.Figure()
    for i in sud3["date"].unique():
        data = sud3[sud3["date"] == i]
        fig.add_trace(go.Bar(
            name=i,
            x=data["subj"],
            y=data["total_marks"],
            customdata=np.transpose(
                [data["ia_marks"], data["main_marks"], data["result"]]),
            texttemplate="%{customdata[0]} + %{customdata[1]} = %{y}  (%{customdata[2]})",
            textposition="auto",
            textangle=270,
            textfont_color="white",
            hovertext=sud3[sud3["date"] == i]["main_marks"],

        ))

    # Change the bar mode
    fig.update_layout(
        title=f"USN : {usn} ({sem})",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='TOTAL MARKS',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargroupgap=0.08,
    )
    html = fig.to_html(include_mathjax="cdn", include_plotlyjs="cdn")
    return html


def result_bar2(sud3, usn, sem):
    fig = px.bar(sud3, x="subj", y="main_marks", barmode="group", color="date", animation_frame="sem",
                 text="result")
    fig.update_layout(
        title=f"USN : {usn} ({sem})",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='TOTAL MARKS',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),

    )
    html = fig.to_html(include_mathjax="cdn", include_plotlyjs="cdn")
    return html
