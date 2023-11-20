from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from user.models import User
from .models import Category, Question, Choice


@admin.register(Category)
class CategoryModelAdmin(ImportExportModelAdmin):
    list_display = ("title", "description")



@admin.register(Question)
class QuestionModelAdmin(ImportExportModelAdmin):
    list_display = ("display_category_title","category", "question")

    def display_category_title(self,obj):
        return obj.category.title

    display_category_title.short_description = 'Category title'

@admin.register(Choice)
class ChoiceModelAdmin(ImportExportModelAdmin):
    list_display = ("display_question_title", "answer", "is_correct")

    def display_question_title(self, obj):
        return obj.question.title

    display_question_title.short_description = 'Question Title'


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'is_active', 'is_staff')
    search_fields = ('full_name', 'username', 'email')


admin.site.register(User, UserAdmin)