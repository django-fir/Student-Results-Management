from django.contrib import admin
from django.utils.html import format_html
from django.db import models

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    code = models.CharField(max_length=10)
    credits = models.IntegerField(default=1)

    def __str__(self):
        return self.code


class ExamMode(models.Model):
    name = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    usn = models.CharField(max_length=10, default="1VI", unique=True)
    # sem = models.ForeignKey(Sem, on_delete=models.CASCADE)
    section = models.CharField(max_length=1, choices=(
        ("A", "A"), ("B", "B"), ("C", "C")), default="A")
    phone_no = models.CharField(max_length=10, default="0000000000")
    spass = models.IntegerField(default=0)
    sfail = models.IntegerField(default=0)
    cgpa = models.IntegerField(default=0)
    branch = models.CharField(max_length=10)
    batch = models.CharField(max_length=10)
    date_of_birth = models.DateField(default="2001-01-26")
    email = models.EmailField()
    father_name = models.CharField(max_length=100)
    father_no = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=(
        ("MALE", "Male"), ("FEMALE", "Female")))
    idd = models.CharField(max_length=100)
    address = models.TextField(max_length=200, default="Laniyaka supercluster")

    def __str__(self):
        return self.usn


class Pre_Records(models.Model):
    name = models.CharField(max_length=50, default="Unknown")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    obtained_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=100)
    percentage = models.IntegerField(default=0)
    passing_month = models.CharField(max_length=20, default="Unknown")
    collage = models.CharField(max_length=100, default="Unknown")
    # cred = models.CharField(max_length=100, default="00000000")

    def __str__(self):
        return self.student.usn


class Example(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sem = models.CharField(max_length=10, choices=(("1", "1st"), ("2", "2nd"), (
        "3", "3rd"), ("4", "4th"), ("5", "5th"), ("6", "6th"), ("7", "7th"), ("8", "8th"), ("9", "9th"), ("10", "10th")), default="1")
    exam_type = models.ForeignKey(ExamMode, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ia_marks = models.IntegerField()
    main_marks = models.IntegerField()
    entry_date = models.DateField(editable=False, auto_now_add=True)
    total_marks = models.IntegerField()
    result = models.CharField(max_length=10, choices=(
        ("P", "Pass"), ("F", "Fail"), ("A", "Absent")), default="P")

    @admin.display
    def result_(self):
        color = "#03fca5"
        text = "Absent"
        if self.result == "P":
            color = "#03fca5"
            text = "Pass"
        elif self.result == "F":
            color = "red"
            text = "Fail"
        else:
            color = "blue"

        return format_html(
            f'<span style="color: {color};">{text}</span>',

        )

    # def get_result(self):
    #     if self.exam_type.min_marks <= self.obtained_marks:
    #         self.result = "Pass"
    #     elif(self.obtained_marks < 0):
    #         self.result = "Absent"
    #     else:
    #         self.result = "Fail"

    # def save(self, *args, **kwargs):
    #     # self.get_result()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.student.name


class ImportExport(models.Model):
    usn = models.CharField(max_length=100)
    sem = models.CharField(max_length=10, choices=(("1", "1st"), ("2", "2nd"), (
        "3", "3rd"), ("4", "4th"), ("5", "5th"), ("6", "6th"), ("7", "7th"), ("8", "8th"), ("9", "9th"), ("10", "10th")), default="1")
    exam_type = models.CharField(max_length=100)

    subject = models.CharField(max_length=100)
    obtained_marks = models.IntegerField()
    exam_date = models.DateField()
    result = models.CharField(max_length=10, choices=(
        ("Pass", "Pass"), ("Fail", "Fail"), ("Absent", "Absent")), default="Pass")

    # def create_entry(self):
    #     stu = Student.objects.get_or_create(usn=self.usn)[0]
    #     exam_type = ExamMode.objects.get_or_create(
    #         name=EName.objects.get_or_create(name=self.exam_type)[0])[0]
    #     sub = Subject.objects.get_or_create(
    #         code=self.subject, sem=Sem.objects.get_or_create(name=self.sem)[0])[0]
    #     Example.objects.update_or_create(student=stu, exam_type=exam_type, sem=self.sem, subject=sub, obtained_marks=self.obtained_marks,
    #                                      exam_date=self.exam_date,

    #                                      result=self.result)

    # def save(self, *args, **kwargs):
    #     self.create_entry()
    #     super().save(*args, **kwargs)
    #     self.delete()
