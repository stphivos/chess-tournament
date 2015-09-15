from django.utils import timezone
from django.db import models, transaction


class ModelBase(object):
    pass


class Participant(ModelBase, models.Model):
    name = models.CharField(max_length=100)
    rating = models.BigIntegerField()
    avatar = models.CharField(max_length=250, default='')

    class Meta:
        db_table = 'chess_participant'


class Game(ModelBase, models.Model):
    no = models.IntegerField()
    round = models.IntegerField()
    start_date = models.DateTimeField(blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True)
    tournament = models.ForeignKey('Tournament', related_name='games')

    p1 = models.ForeignKey('Participant', related_name='games_1')
    p1_score = models.FloatField(null=True)
    p1_start_elo = models.BigIntegerField()
    p1_end_elo = models.BigIntegerField(null=True)

    p2 = models.ForeignKey('Participant', related_name='games_2')
    p2_score = models.FloatField(null=True)
    p2_start_elo = models.BigIntegerField()
    p2_end_elo = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'chess_game'

    @property
    def winner(self):
        if self.p1_score > self.p2_score:
            return self.p1
        elif self.p2_score > self.p1_score:
            return self.p2
        else:
            return self.p1

    @property
    def loser(self):
        if self.p1_score < self.p2_score:
            return self.p1
        elif self.p2_score < self.p1_score:
            return self.p2
        else:
            return self.p2

    @transaction.atomic
    def finish(self, p1_score, p2_score):
        if self.end_date:
            raise Exception('Game has already finished.')

        self.p1_score = p1_score
        self.p2_score = p2_score
        self.end_date = timezone.now()
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.p1_start_elo:
            self.p1_start_elo = self.p1.rating
        if not self.p2_start_elo:
            self.p2_start_elo = self.p2.rating

        if self.end_date and not self.p1_end_elo:
            self.p1_end_elo = self.calculate_rating(self.p1_start_elo, self.p2_start_elo, self.p1_score)
        if self.end_date and not self.p2_end_elo:
            self.p2_end_elo = self.calculate_rating(self.p2_start_elo, self.p1_start_elo, self.p2_score)

        super(Game, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)

    def calculate_rating(self, p_rating, other_rating, p_score):
        k = self.tournament.k_factor
        r1 = 10 ** (p_rating / 400)
        r2 = 10 ** (other_rating / 400)
        e = r1 / (r1 + r2)
        r = r1 + k * (p_score - e)
        return int(r)


class TournamentParticipant(ModelBase, models.Model):
    tournament = models.ForeignKey('Tournament')
    participant = models.ForeignKey('Participant')

    class Meta:
        db_table = 'chess_tournament_participant'

    def __init__(self, tournament=None, participant=None):
        super(TournamentParticipant, self).__init__()
        self.tournament = tournament
        self.participant = participant


class Tournament(ModelBase, models.Model):
    start_date = models.DateTimeField(blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True)
    rounds = models.IntegerField()
    current_round = models.IntegerField(default=0)
    k_factor = models.IntegerField()
    participants = models.ManyToManyField(Participant, through='TournamentParticipant')

    class Meta:
        db_table = 'chess_tournament'

    @property
    def started(self):
        return self.games.count() > 0

    @property
    def is_round_completed(self):
        round_games = [x for x in self.games.all() if x.round == self.current_round]
        finished_games = [x for x in round_games if x.end_date]
        return len(round_games) == len(finished_games)

    @property
    def has_more_rounds(self):
        return self.current_round < self.rounds

    @transaction.atomic
    def start(self, participant_ids):
        if self.current_round != 0:
            raise Exception('Tournament has already started.')

        self.current_round = 1

        participants = list(Participant.objects.filter(pk__in=participant_ids).all())
        for p in participants:
            self.tournamentparticipant_set.add(TournamentParticipant(tournament=self, participant=p))

        # participants = self.participants.order_by('-rating').all()
        participants = sorted(participants, key=lambda x: x.rating, reverse=True)

        group_size = len(participants) / 2
        top_half = participants[:group_size]
        bottom_half = participants[group_size:]

        for i in range(group_size):
            game = Game()
            game.no = i + 1
            game.tournament = self
            game.round = self.current_round
            game.p1 = top_half[i]
            game.p2 = bottom_half[i]
            game.save()

        self.save()

    @transaction.atomic
    def advance(self):
        # games = self.games.filter(round=self.current_round).all()
        games = list(self.games.filter(round=self.current_round).all().select_related('p1', 'p2'))
        if len(games) < 1:
            raise Exception('Tournament has ended.')

        self.current_round += 1

        winners = [x.winner for x in games if x.end_date]
        losers = [x.loser for x in games if x.end_date]

        if len(winners) < len(games) or len(losers) < len(games):
            raise Exception('There are games in this round that are still pending.')

        offset = len(games) / 2

        for i in range(offset):
            game = Game()
            game.no = i + 1
            game.tournament = self
            game.round = self.current_round
            game.p1 = winners[i]
            game.p2 = winners[i + offset]
            game.save()

        if offset == 0:
            self.end_date = timezone.now()

        self.save()
