from os import listdir, path
from django import forms
from djangular.forms import NgFormValidationMixin, NgModelForm
from djangular.styling.bootstrap3.forms import Bootstrap3FormMixin
from chess_tournament.settings import AVATAR_ROOT
from judge_interface.models import Participant, Tournament


def get_avatars():
    return [(x, path.splitext(x)[0]) for x in listdir(AVATAR_ROOT)]


class ParticipantForm(Bootstrap3FormMixin, NgFormValidationMixin, NgModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'rating', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'ng-model': 'request.name'}),
            'rating': forms.NumberInput(attrs={'ng-model': 'request.rating'}),
            'avatar': forms.Select(attrs={'ng-model': 'request.avatar'}, choices=get_avatars())
        }


class TournamentForm(Bootstrap3FormMixin, NgFormValidationMixin, NgModelForm):
    class Meta:
        model = Tournament
        fields = ['rounds', 'k_factor']
        widgets = {
            'rounds': forms.NumberInput(attrs={'ng-model': 'request.rounds'}),
            'k_factor': forms.NumberInput(attrs={'ng-model': 'request.k_factor'})
        }
