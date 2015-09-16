from django.conf.urls import url, include
from rest_framework import routers
from judge_interface import views

router = routers.DefaultRouter()
router.register(r'participants', views.ParticipantViewSet, base_name='participants')
router.register(r'tournament', views.TournamentViewSet, base_name='tournament')

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),

    url(r'^login', views.LoginView.as_view(), name='login'),

    url(r'^participant/edit', views.ParticipantEditView.as_view(), name='participant_edit'),
    url(r'^participants', views.ParticipantsView.as_view(), name='participants'),

    url(r'^tournament/edit', views.TournamentEditView.as_view(), name='tournament_edit'),
    url(r'^tournament/start', views.TournamentStartView.as_view(), name='tournament_start'),
    url(r'^tournament', views.TournamentView.as_view(), name='tournament'),

    url(r'^api/tournament/(?P<tour>\d+)/round/(?P<round>\d+)/game/(?P<no>\d+)', views.GameFindView.as_view(),
        name='game_find'),
    url(r'^api/game/(?P<id>\d+)/p1/(?P<p1>\d+(\.\d)?)/p2/(?P<p2>\d+(\.\d)?)', views.GameEndView.as_view(),
        name='game_end'),

    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
