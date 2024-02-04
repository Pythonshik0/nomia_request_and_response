from django.shortcuts import render, redirect
from .models import Survey, Question, Response, Choice, QuestionChoice
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection


def home_page(request):
    surveys = Survey.objects.all()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(DISTINCT user_id) AS total_participants " 
            "FROM public.\"QUESTIONS_response\";"
        )
        total_participants = cursor.fetchone()[0]

        cursor.execute(
            "WITH question_counts AS (\
                SELECT question_id, COUNT(user_id) AS total_respondents \
                FROM public.\"QUESTIONS_response\" \
                GROUP BY question_id \
            ) \
            SELECT main.question_id, \
                main.choice_id, \
                COUNT(main.user_id) AS choice_respondents, \
                ROUND(COUNT(main.user_id)*100.0 / qc.total_respondents, 2) AS choice_percentage \
            FROM public.\"QUESTIONS_response\" main \
            JOIN question_counts qc ON main.question_id = qc.question_id \
            GROUP BY main.question_id, main.choice_id, qc.total_respondents;"
        )
        choice_respondents = cursor.fetchall()

        formatted_results = [
            f"(Вопрос: {row[0]}, \
            Вариант ответа: {row[1]}, \
            Количество ответивших: {row[2]}, \
            % ответило: {row[3]:.2f})"
            for row in choice_respondents
        ]

        context = {
            'surveys': surveys,
            'total_participants': total_participants,
            'formatted_results': formatted_results,
        }

    return render(request, 'home_page.html', context)


def error(request):
    return render(request, 'error.html')


@login_required
def survey(request, survey, question_number):
    selected_survey = Survey.objects.get(title=survey)
    try:  # Если вопроса таким id нет
        question = Question.objects.get(survey=selected_survey, id=question_number)
    except Exception:
        question_number += 1
        question = Question.objects.get(survey=selected_survey, id=question_number)

    question_choice = QuestionChoice.objects.filter(
        question=question)  # Получаем все варианты ответов для выбранного вопроса

    try:  # Чтобы ответы нельзя было записать больше одного раза
        check_question_programmist = Response.objects.get(user=request.user, survey=selected_survey, question=question)
        return render(request, 'error.html')
    except Exception:
        if request.method == 'POST':
            selected_choice_id = request.POST.get(
                f'answer_{question.id}')  # Получаем id выбранного варианта из POST-запроса
            selected_choice = Choice.objects.get(id=selected_choice_id)  # Получаем выбранный вариант по id
            response = Response(user=request.user, survey=selected_survey, question=question, choice=selected_choice)
            response.save()
            if question_number >= 7:
                user_responses = Response.objects.filter(user=request.user)
                return render(request, 'response.html', {'user_responses': user_responses})

            if question_number == 6:
                check_question_programmist = Response.objects.get(user=request.user, survey=selected_survey, question=2)
                check_question_programmist_prof = Response.objects.get(user=request.user, survey=selected_survey, question=6)
                if check_question_programmist.choice.text == 'От 18 до 25' and check_question_programmist_prof.choice.text == 'Программист':
                    question_number = 7
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 25 до 45' and check_question_programmist_prof.choice.text == 'Программист':
                    question_number = 8
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 45 и более' and check_question_programmist_prof.choice.text == 'Программист':
                    question_number = 9
                    return redirect('survey', survey=survey, question_number=question_number)

                elif check_question_programmist.choice.text == 'От 18 до 25' and check_question_programmist_prof.choice.text == 'Политик':
                    question_number = 10
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 25 до 45' and check_question_programmist_prof.choice.text == 'Политик':
                    question_number = 11
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 45 и более' and check_question_programmist_prof.choice.text == 'Политик':
                    question_number = 12
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 18 до 25' and check_question_programmist_prof.choice.text == 'Дизайнер одежды':
                    question_number = 13
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 25 до 45' and check_question_programmist_prof.choice.text == 'Дизайнер одежды':
                    question_number = 14
                    return redirect('survey', survey=survey, question_number=question_number)
                elif check_question_programmist.choice.text == 'От 45 и более' and check_question_programmist_prof.choice.text == 'Дизайнер одежды':
                    question_number = 15
                    return redirect('survey', survey=survey, question_number=question_number)

            elif question_number < 6:
                question_number += 1
                return redirect('survey', survey=survey, question_number=question_number)

        return render(request, 'survey.html',
                      {'question': question, 'selected_survey': selected_survey, 'question_choice': question_choice,
                       'question_number': question_number})


