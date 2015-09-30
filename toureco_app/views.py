from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question, Choice
from .forms import (AccompanyForm, AccompanyNumForm, StayPeriodForm,
    MotiveForm, ExpenseForm, WeightForm)
from .choice import choice_accompany
from core import pretreatment2


def index(request):
    return render(request, 'toureco_app/index.html')


def welcome(request):
    ctx = {'next_count': 1}

    # clear the request session
    request.session.clear()

    return render(request, 'toureco_app/welcome.html', ctx)


# choice conditions on multiple-level
def choice(request, next_count):
    forms = [None, AccompanyForm, AccompanyNumForm, StayPeriodForm, MotiveForm,
        ExpenseForm, WeightForm]
    response_pages = [None, 'choice_accompany.html', 'choice_accompany_num.html',
        'choice_stay_period.html', 'choice_motive.html','choice_expense.html',
        'choice_weight.html']

    counter = int(next_count)

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
                    request.session[key] = value[0]
                # print request.session.items()
            counter += 1

            return redirect('toureco_app:choice', next_count=counter)
        else:
            is_error = True

    if counter == len(forms):
        return redirect('toureco_app:view_reco')

    if not is_error:
        form = forms[counter]

    response_page = '/'.join(['toureco_app', response_pages[counter]])

    ctx = {'form': form, 'next_count': counter}

    return render(request, response_page, ctx)


def view_reco_result(request):
    con_dict = {}
    reco_dict = {}
    ctx = None

    for key, value in request.session.items():
        con_dict[key] = int(value)

    # recommendation processing
    # reco_dict = pretreatment2.reco_wizard(con_dict['motive_of_tour_1'],
    #     con_dict['motive_of_tour_2'], con_dict['motive_of_tour_3'],
    #     con_dict['accompany_kind'], con_dict['accompany_num'],
    #     con_dict['stay_period'], con_dict['expense_of_all_per_man'],
    #     con_dict['weight_lodging'], con_dict['weight_shopping'],
    #     con_dict['weight_food'], con_dict['weight_transport'],
    #     con_dict['weight_entertainment'], con_dict['weight_culture'])

    ctx = {'condition_data': con_dict, 'reco_data': reco_dict}

    return render(request, 'toureco_app/view_reco.html', ctx)
