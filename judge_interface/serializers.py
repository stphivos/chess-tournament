from django.contrib.auth.models import User
from judge_interface.models import Participant, Game, Tournament
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    score = serializers.SerializerMethodField()
    round = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ('id', 'name', 'rating', 'avatar', 'score', 'round',)

    def get_score(self, participant):
        return participant.score if hasattr(participant, 'score') else 0

    def get_round(self, participant):
        return participant.round if hasattr(participant, 'round') else 0


class GameSerializer(serializers.HyperlinkedModelSerializer):
    p1 = ParticipantSerializer()
    p2 = ParticipantSerializer()

    class Meta:
        model = Game
        fields = ('id', 'round', 'no', 'start_date', 'end_date', 'p1', 'p1_score', 'p2', 'p2_score',)


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    __games = None

    players = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()
    winner = ParticipantSerializer(read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'start_date', 'end_date', 'rounds', 'current_round', 'k_factor', 'players', 'games', 'winner',)

    def get_players(self, tournament):
        players = []

        if not self.__games:
            self.__games = list(tournament.games.order_by('-round', 'no').all().select_related('p1', 'p2'))

        def update_players(game, player, score):
            if player not in players:
                player.score = score
                player.round = game.round
                player.opponents = player.get_opponents_total(self.__games)
                players.append(player)
                return True
            return False

        for g in [x for x in self.__games if x.end_date]:
            if g.p1:
                update_players(g, g.p1, g.p1_total_score)
            if g.p2:
                update_players(g, g.p2, g.p2_total_score)

        values = sorted(players, key=lambda x: (x.score, x.opponents), reverse=True)
        return ParticipantSerializer(instance=values, many=True).data

    def get_games(self, tournament):
        if not self.__games:
            self.__games = list(tournament.games.order_by('-round', 'no').all().select_related('p1', 'p2'))

        games = [x for x in self.__games if x.p1 and x.p2 and x.round == tournament.current_round]

        return GameSerializer(instance=games, many=True).data
