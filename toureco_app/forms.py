from django.core.exceptions import ValidationError
from django import forms
import choice


# validate functions
def validate_positive(value):
    if value < 1:
        raise ValidationError("value must be positive")


def validate_non_negative(value):
    if value < 0:
        raise ValidationError("value must be non negative")


def validate_only_3_select(values):
    if len(values) != 3:
        raise ValidationError("select only 3 items")


# form classess
class AccompanyForm(forms.Form):
    accompany_kind = forms.ChoiceField(choices=choice.choice_accompany,
        required=True, help_text='select accompany',
        error_messages={'required': 'select please'},
        widget=forms.Select(attrs={'class': 'choice'}))


class AccompanyNumForm(forms.Form):
    accompany_num = forms.IntegerField(required=True, help_text='type number',
        error_messages={'required': 'type please'},
        min_value=1, validators=[validate_positive])


class StayPeriodForm(forms.Form):
    stay_period = forms.IntegerField(required=True, help_text='type period',
        error_messages={'required': 'type please'},
        min_value=1, validators=[validate_positive])


class MotiveForm(forms.Form):
    motive_of_tour = forms.MultipleChoiceField(choices=choice.choice_motive,
        required=True, help_text="select motives",
        error_messages={'required': 'select 3 motives'},
        validators=[validate_only_3_select],
        widget=forms.SelectMultiple(attrs={'size': len(choice.choice_motive) + 2,
            'multiple': 'multiple', 'class': 'choice limit-select'}))


class ExpenseForm(forms.Form):
    expense_of_all_per_man = forms.IntegerField(required=True, help_text='type expense',
        error_messages={'required': 'type please'},
        min_value=0, validators=[validate_non_negative])
