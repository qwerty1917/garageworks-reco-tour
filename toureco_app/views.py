from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question, Choice
from .forms import (AccompanyForm, AccompanyNumForm, StayPeriodForm,
    MotiveForm, ExpenseForm)
from .choice import choice_accompany

def index(request):
    return render(request, 'toureco_app/index.html')


def welcome(request):
    ctx = {'next_count': 1}

    # clear the request session
    request.session.clear()

    return render(request, 'toureco_app/welcome.html', ctx)


# choice conditions on multiple-level
def choice(request, next_count):
    forms = [AccompanyForm, AccompanyNumForm, StayPeriodForm, MotiveForm,
        ExpenseForm]
    response_pages = ['choice_accompany.html', 'choice_accompany_num.html',
        'choice_stay_period.html', 'choice_motive.html','choice_expense.html']

    counter = int(next_count)-1

    form = None
    ctx = None
    response_page = None
    is_error = False

    if request.method == 'POST':
        form = forms[counter](request.POST)
        if form.is_valid():
            for key, value in request.POST.iterlists():
                if len(value) > 1:
                    for idx, sub in enumerate(value):
                        request.session['_'.join([key, str(idx + 1)])] = value[idx]
                else:
                    request.session[key] = value
            print request.session.items()
            counter += 1
        else:
            is_error = True

    if not is_error:
        form = forms[counter]

    response_page = '/'.join(['toureco_app', response_pages[counter]])

    ctx = {'form': form, 'next_count': counter + 1}

    return render(request, response_page, ctx)
