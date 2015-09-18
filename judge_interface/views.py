from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView
from judge_interface.application import ApplicationService
from judge_interface.forms import ParticipantForm, TournamentForm, LoginForm
from judge_interface.infrastructure import json_result, template_result
from judge_interface.models import Participant, Game, Tournament
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from judge_interface.serializers import UserSerializer, ParticipantSerializer, TournamentSerializer, GameSerializer


class ApiMixin(object):
    __app_service = None

    @property
    def app_service(self):
        if not self.__app_service:
            self.__app_service = ApplicationService()
        return self.__app_service


class AuthenticationMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticationMixin, self).dispatch(*args, **kwargs)


class ViewBase(ApiMixin, TemplateView):
    @property
    def last_feedback(self):
        return self.request.session['last_feedback'] if 'last_feedback' in self.request.session else None

    @last_feedback.setter
    def last_feedback(self, value):
        self.request.session['last_feedback'] = value

    def get_context_data(self, **kwargs):
        kwargs.update(last_feedback=self.last_feedback)
        self.last_feedback = None
        return super(ViewBase, self).get_context_data(**kwargs)


class FormViewBase(ViewBase, FormView):
    success_url = '/'
    form_class = None

    def get_context_data(self, **kwargs):
        kwargs.update(form=self.get_form() if 'form' not in kwargs else kwargs['form'])
        return super(FormViewBase, self).get_context_data(**kwargs)

    def form_valid(self, form):
        overwritten_result = self.success_action(form)
        original_result = super(FormViewBase, self).form_valid(form)
        return original_result if overwritten_result is None else overwritten_result

    def success_action(self, form):
        pass


class HomeView(ViewBase):
    template_name = 'home/index.html'


class LoginView(ApiMixin, generics.ListCreateAPIView):
    @template_result
    def get(self, request, *args, **kwargs):
        return 'home/login.html' if request.is_ajax() else 'home/index.html', {'form': LoginForm()}

    @json_result
    def post(self, request, *args, **kwargs):
        self.app_service.authenticate(request, request.POST['username'], request.POST['password'])


class ParticipantsView(ViewBase):
    def get(self, request, *args, **kwargs):
        self.template_name = 'chess/participants.html' if request.is_ajax() else 'home/index.html'
        return super(ParticipantsView, self).get(request, *args, **kwargs)


class ParticipantEditView(FormViewBase):
    template_name = 'chess/participant_editor.html'
    form_class = ParticipantForm

    def get_form_kwargs(self):
        kwargs = super(ParticipantEditView, self).get_form_kwargs()
        if 'id' in self.request.GET:
            kwargs.update(instance=Participant.objects.get(pk=self.request.GET['id']))
        return kwargs


class TournamentView(ViewBase):
    def get(self, request, *args, **kwargs):
        self.template_name = 'chess/tournament.html' if request.is_ajax() else 'home/index.html'
        return super(TournamentView, self).get(request, *args, **kwargs)


class TournamentEditView(FormViewBase):
    template_name = 'chess/tournament_editor.html'
    form_class = TournamentForm

    def get_form_kwargs(self):
        kwargs = super(TournamentEditView, self).get_form_kwargs()
        if 'id' in self.request.GET:
            kwargs.update(instance=Tournament.objects.get(pk=self.request.GET['id']))
        return kwargs


class TournamentStartView(generics.CreateAPIView):
    """
    API endpoint that allows tournaments to start.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        participants = list(map(int, request.POST['ids'].split(',')))
        tournament = Tournament.objects.all().order_by('-start_date').first()
        tournament.start(participants)
        return JsonResponse({})


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows participants to be viewed or edited.
    """
    queryset = Participant.objects.all().order_by('name')
    serializer_class = ParticipantSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tournaments to be viewed or edited.
    """
    queryset = Tournament.objects.all().order_by('-start_date')
    serializer_class = TournamentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def get_object(self):
        return self.get_queryset().first()


class GameFindView(generics.RetrieveAPIView):
    """
    API endpoint that allows games to be viewed.
    """
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return Game.objects.filter(
            tournament_id=self.kwargs['tour'],
            round=self.kwargs['round'],
            no=self.kwargs['no']).select_related('p1', 'p2').first()


class GameEndView(generics.UpdateAPIView):
    """
    API endpoint that allows games to be updated.
    """
    queryset = Game.objects.all().select_related('tournament')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        game = self.get_object()
        game.finish(float(kwargs['p1']), float(kwargs['p2']))

        if game.tournament.is_round_completed:
            if game.tournament.has_more_rounds:
                game.tournament.advance()
            else:
                game.tournament.finish()

        return Response({})
