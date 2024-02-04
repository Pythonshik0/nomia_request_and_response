from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    title_topic = models.CharField(max_length=30)

    def __str__(self):
        return f'Опрос: {self.title}, тема:{self.title_topic}'


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    def __str__(self):
        return f'Вопрос: {self.text}'


class Choice(models.Model):
    text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'Ответ: {self.text}'


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ответ от {self.user}: {self.choice}.' \
               f'\n На вопрос: {self.question}' \
               f'\n На опрос: {self.survey}'