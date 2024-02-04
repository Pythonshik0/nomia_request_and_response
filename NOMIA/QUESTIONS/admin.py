from django.contrib import admin
from .models import Survey, Question, Choice, Response, QuestionChoice


class RecipeProductInline(admin.TabularInline):
    model = QuestionChoice  # Используем нашу промежуточную модель вместо through-модели
    extra = 3
    fields = ['question', 'choice']


admin.site.register(Survey)
admin.site.register(Response)


@admin.register(Question)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]


admin.site.register(Choice)
admin.site.register(QuestionChoice)
