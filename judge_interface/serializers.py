from django.contrib.auth.models import User
from judge_interface.models import Participant, Game, Tournament
from rest_framework import serializers
from random import randint


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name', 'rating', 'avatar',)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    p1 = ParticipantSerializer()
    p2 = ParticipantSerializer()

    class Meta:
        model = Game
        fields = ('id', 'start_date', 'end_date', 'p1', 'p1_score', 'p2', 'p2_score',)


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    tree = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ('id', 'start_date', 'end_date', 'rounds', 'k_factor', 'tree',)

    def get_empty(self):
        p = Participant()
        p.id = randint(1000000, 10000000)
        return p

    def get_json(self, participant):
        return {
            'name': participant.name if participant.name else '',
            'id': participant.id,
            'seed': participant.id if participant.name else ''
        }

    def get_tree(self, tournament):
        data = []
        participant_count = tournament.participants.count()
        game_count = participant_count / 2
        all_games = list(tournament.games.order_by('no').all().select_related('p1', 'p2'))

        for r in range(1, tournament.rounds + 1):
            # games = tournament.games.order_by('no').filter(round=r).all()
            games = [x for x in all_games if x.round == r]
            pairs = []

            for i in range(game_count):
                matches = [x for x in games if x.no == i + 1]
                p1 = matches[0].p1 if len(matches) > 0 else self.get_empty()
                p2 = matches[0].p2 if len(matches) > 0 else self.get_empty()
                pairs.append([self.get_json(p1), self.get_json(p2)])

            if game_count == 0:
                # final = tournament.games.filter(round=tournament.rounds - 1).first()
                final = [x for x in all_games if x.round == tournament.rounds - 1]
                if len(final) > 0 and final[0].end_date:
                    pairs.append([self.get_json(final[0].winner)])

            if participant_count > 0 and len(pairs) == 0:
                pairs.append([self.get_json(self.get_empty())])

            if len(pairs) > 0:
                data.append(pairs)

            game_count /= 2

        return data if len(data) > 0 else None
