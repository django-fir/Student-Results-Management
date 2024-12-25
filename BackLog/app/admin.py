from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin
from .models import *
# Register your models here.
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class SubjectList(SimpleListFilter):
    title = _('subject')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'subject'

    def result_render(self, sub_listt):
        sub_list = []
        dup = []
        for i in sub_listt:
            if i["subject__id"] not in dup:
                dup.append(i["subject__id"])
                color = "#03fca5"
                if i["result"] == "P":
                    color = "#03fca5"
                elif i["result"] == "F":
                    color = "#f54f40"
                else:
                    color = "blue"
                sub_list.append((i["subject__id"], format_html(
                    f"<span style='color:{color}';>{i['subject__code']}</span>")))
        return sub_list

    def lookups(self, request, model_admin):
        print(request.GET, model_admin)
        sub_list = []
        print(request.GET.get("q"))
        if request.GET.get("q") and request.GET.get("sem__exact"):
            sub_listt = model_admin.model.objects.filter(student__usn__iexact=request.GET.get("q"), sem__iexact=request.GET.get("sem__exact", '')).values(
                "subject__id", "subject__code", "result", "exam_type").order_by("-exam_type")
            sub_list = self.result_render(sub_listt)

        elif request.GET.get("sem__exact"):
            sub_list = set((i["subject__id"], i["subject__code"])
                           for i in model_admin.model.objects.filter(sem=request.GET.get("sem__exact", "")).values("subject__id", "subject__code"))

        else:
            # sub_list = set((i["subject__id"], i["subject__code"])
            #                for i in model_admin.model.objects.filter(student__usn=request.GET.get("q")).values("subject__id", "subject__code"))
            sub_listt = model_admin.model.objects.filter(student__usn__iexact=request.GET.get("q")).values(
                "subject__id", "subject__code", "result", "exam_type").order_by("-exam_type")
            sub_list = self.result_render(sub_listt)

        return sub_list

    def queryset(self, request, queryset):
        print(request.GET, queryset)
        if request.GET.get("q") and request.GET.get("sem__exact") and request.GET.get("subject"):
            return queryset.filter(student__usn__iexact=request.GET.get("q", ''), sem__iexact=request.GET.get("sem__exact", ''), subject__id=request.GET.get("subject", ''))
        elif request.GET.get("sem__exact"):
            return queryset.filter(sem__iexact=request.GET.get("sem__exact", ''))
        else:
            return queryset


class ExampleAdmin(admin.ModelAdmin):
    list_display = ["view_name",
                    "student",
                    "subject_",
                    "exam_type",
                    "ia_marks",
                    "main_markss",
                    "total_marks",
                    "result_",
                    "sem",
                    ]
    list_display_links = ["view_name", "student"]
    # list_editable = [
    #     "subject",
    #     "exam_type",
    #     "exam_date",
    #     "obtained_marks",
    #     "result",
    #     "sem",
    # ]
    date_hierarchy = 'entry_date'
    empty_value_display = '-empty-'
    list_filter = ["result", "sem", "student__batch", SubjectList]
    radio_fields = {"exam_type": admin.HORIZONTAL}
    search_fields = ["student__usn"]
    autocomplete_fields = ["student", "subject"]
    fieldsets = (
        (None, {
            'fields': (("student",
                        "subject",),
                       "exam_type",
                       )
        }),
        ('Advanced options', {
            'classes': ('wide', 'extrapretty'),
            'fields': ("main_marks",
                       "ia_marks",
                       "result",
                       "sem",),
        }),
    )

    @ admin.display(empty_value='???')
    def view_name(self, obj):
        return format_html(f'<span style="color:orange;">{obj.student.name}</span>')

    # @ admin.display(empty_value='???')
    # def Exam_Type(self, obj):
    #     if obj.exam_type.name.name == "MAIN-1":
    #         color = "#b500f7"
    #     elif obj.exam_type.name.name == "MAIN-1-R":
    #         color = "#ffc003"
    #     else:
    #         color = "pink"
    #     return format_html(f'<span style="color:{color};">{obj.exam_type}</span>')

    @ admin.display(empty_value='???')
    def main_markss(self, obj):
        color = "#03fca5"
        if obj.result == "P":
            color = "#03fca5"
        elif obj.result == "F":
            color = "#f54f40"
        else:
            color = "blue"
        return format_html(f'<span style="color:{color};">{obj.main_marks}</span>')

    @ admin.display(empty_value='???')
    def subject_(self, obj):
        color = "#03fca5"
        if obj.result == "P":
            color = "#03fca5"
        elif obj.result == "F":
            color = "#f54f40"
        else:
            color = "blue"
        return format_html(f'<span style="color:{color};">{obj.subject}</span>')


class ExamAdminAdmin(admin.StackedInline):
    model = Example
    autocomplete_fields = ["student", "subject"]
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    inlines = [ExamAdminAdmin]
    list_display = ["name", "usn", "phone_no",
                    "branch", "batch", "spass", "sfail", "cgpa"]
    search_fields = ["usn", "name"]


class SemAdmin(admin.ModelAdmin):
    list_display = ["name"]


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    search_fields = ["code"]


class ExamModeAdmin(admin.ModelAdmin):
    list_display = ["name"]


class Exam_ResultAdmin(admin.ModelAdmin):
    list_display = ["student",
                    "subject",
                    "Emode",
                    "exam_date",
                    "obtained_marks",
                    "result"]


class ENameAdmin(admin.ModelAdmin):
    list_display = ["name"]


# admin.site.register(EName, ENameAdmin)
admin.site.register(Subject, SubjectAdmin)
# admin.site.register(Sem, SemAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ExamMode, ExamModeAdmin)
admin.site.register(Example, ExampleAdmin)


class BookResource(resources.ModelResource):

    class Meta:
        model = ImportExport
        # fields = ("id","usn", "sem", "exam_type", "subject",
        #           "obtained_marks", "exam_date", "result")
        # import_id_fields = ('id',)
        # exclude = ("created",)


class bookadminie(ImportExportActionModelAdmin):
    list_display = ["usn",
                    "subject",
                    "exam_type",
                    "exam_date",
                    "obtained_marks",
                    "result",
                    "sem"]
    resource_classes = [BookResource]


admin.site.register(ImportExport, bookadminie)
admin.site.register(Pre_Records)
