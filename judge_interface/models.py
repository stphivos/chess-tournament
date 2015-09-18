from operator import itemgetter
from django.utils import timezone
from django.db import models, transaction
from itertools import permutations
from random import randrange


class ModelBase(object):
    pass


class Participant(ModelBase, models.Model):
    name = models.CharField(max_length=100)
    rating = models.BigIntegerField()
    avatar = models.CharField(max_length=250, default='')

    class Meta:
        db_table = 'chess_participant'

    def played_with(self, games, player):
        if self == player:
            return True
        return len([x for x in games if (self == x.p1 or self == x.p2) and (player == x.p1 or player == x.p2)]) > 0

    def get_total_score(self, games):
        scores = [x.p1_total_score if self == x.p1 else x.p2_total_score if self == x.p2 else 0 for x in games]
        if len(scores) > 0:
            return sorted(scores, reverse=True)[0]
        else:
            return 0

    def update_rating(self, tournament, games):
        total = count = 0
        for g in games:
            if self in [g.p1, g.p2] and g.p1 and g.p2:
                score = g.p1_score if g.p1 == self else g.p2_score
                other = g.p1 if g.p2 == self else g.p1
                total += self.calculate_rating(tournament, other.rating, score)
                count += 1
        self.rating = int(total / count)

    def calculate_rating(self, tournament, other_rating, p_score):
        k = tournament.k_factor
        r1 = 10 ** (self.rating / 400)
        r2 = 10 ** (other_rating / 400)
        e = r1 / (r1 + r2)
        r = r1 + k * (p_score - e)
        return int(r)

    def get_opponents_total(self, games):
        return sum([x.p1_total_score if x.p2 == self else x.p2_total_score if x.p1 == self else 0 for x in games])


class Game(ModelBase, models.Model):
    no = models.IntegerField()
    round = models.IntegerField()
    start_date = models.DateTimeField(blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True)
    tournament = models.ForeignKey('Tournament', related_name='games')

    p1 = models.ForeignKey('Participant', related_name='games_1', null=True)
    p1_score = models.FloatField(null=True)
    p1_total_score = models.FloatField(null=True)

    p2 = models.ForeignKey('Participant', related_name='games_2')
    p2_score = models.FloatField(null=True)
    p2_total_score = models.FloatField(null=True)

    class Meta:
        db_table = 'chess_game'

    @property
    def winner(self):
        if self.p1_score > self.p2_score:
            return self.p1
        elif self.p2_score > self.p1_score:
            return self.p2
        else:
            return None

    @property
    def loser(self):
        if self.p1_score < self.p2_score:
            return self.p1
        elif self.p2_score < self.p1_score:
            return self.p2
        else:
            return None

    @transaction.atomic
    def finish(self, p1_score, p2_score):
        if self.end_date:
            raise Exception('Game has already finished.')

        self.p1_score = p1_score
        self.p2_score = p2_score
        self.end_date = timezone.now()
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.p1 and self.p1_score:
            self.p1_total_score = self.p1_score + (self.p1_total_score if self.p1_total_score else 0)

        if self.p2 and self.p2_score:
            self.p2_total_score = self.p2_score + (self.p2_total_score if self.p2_total_score else 0)

        super(Game, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)


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
    winner = models.ForeignKey('Participant', blank=True, null=True, related_name='tournaments_won')

    class Meta:
        db_table = 'chess_tournament'

    @property
    def started(self):
        return self.current_round != 0

    @property
    def is_round_completed(self):
        round_games = [x for x in self.games.all() if x.round == self.current_round]
        finished_games = [x for x in round_games if x.end_date]
        return len(round_games) == len(finished_games)

    @property
    def has_more_rounds(self):
        return self.current_round < self.rounds

    def create_game(self, prev_games, no, p1, p2):
        game = Game()
        game.round = self.current_round
        game.tournament = self
        game.no = no
        game.p1 = p1
        game.p2 = p2
        if p1:
            game.p1_total_score = p1.get_total_score(prev_games)
        if p2:
            game.p2_total_score = p2.get_total_score(prev_games)
        return game

    # pair players of the same or similar score group
    @classmethod
    def generate_pairs(cls, players, scores, games):
        pairs = []

        for i, score in enumerate(scores):
            score_players = sorted([p for p in players if players[p] == score], key=lambda x: x.rating, reverse=True)

            if len(score_players) % 2 != 0:  # odd number of players
                if i < len(scores) - 1:
                    next_score_players = [p for p in players if players[p] == scores[i + 1]]
                    highest = sorted(next_score_players, key=lambda x: x.rating, reverse=True)[0]
                    score_players.append(highest)  # add highest ranked player from the next (lower) score group
                    players.pop(highest, None)
                else:  # last score group
                    bye = score_players[-1]
                    score_players.remove(bye)  # or say bye to the lowest ranked player for this round
                    players.pop(bye, None)
                    pairs.append([bye])

            # part group in half and try to match each player with an opponent they haven't faced before
            group_size = len(score_players) / 2
            top_half = score_players[:group_size]
            bottom_half = score_players[group_size:]
            lower_score_players = bottom_half + [k for k, v in players.items() if v < score]

            j = 0
            while len(top_half) > 0 or len(bottom_half) > 0:
                if j >= len(lower_score_players):
                    # No possible pairing for these groups of players.
                    break
                elif not top_half[0].played_with(games, lower_score_players[j]):
                    p1 = top_half[0]
                    p2 = lower_score_players[j]

                    pairs.append([p1, p2])
                    top_half.remove(p1)
                    lower_score_players.remove(p2)

                    if p2 in bottom_half:
                        bottom_half.remove(p2)
                    if len(top_half) == 0:
                        top_half = bottom_half
                        for x in top_half:
                            lower_score_players.remove(x)

                    players.pop(p1, None)
                    players.pop(p2, None)

                    j = 0
                else:
                    j += 1

        return pairs

    @classmethod
    def get_players_and_scores(cls, games):
        scores = [0]
        players = {}
        unfinished = 0

        for x in games:
            if not x.end_date:
                unfinished += 1
            else:
                if x.p1:
                    players[x.p1] = x.p1_total_score
                if x.p2:
                    players[x.p2] = x.p2_total_score
                if x.p1_total_score and x.p1_total_score not in scores:
                    scores.append(x.p1_total_score)
                if x.p2_total_score and x.p2_total_score not in scores:
                    scores.append(x.p2_total_score)

        if unfinished > 0:
            raise Exception('There are games in this round that are still pending.')

        return sorted(scores, reverse=True), players

    # Buchholz tie breaking system
    @classmethod
    def break_tie(cls, games, finalists):
        scores = {}
        for p in finalists:
            total = p.get_opponents_total(games)
            scores[total] = p
        return scores[max(scores.keys())]

    @transaction.atomic
    def start(self, participant_ids):
        if self.started:
            raise Exception('Tournament has already started.')

        self.current_round = 1

        participants = list(Participant.objects.filter(pk__in=participant_ids).all())
        for p in participants:
            self.tournamentparticipant_set.add(TournamentParticipant(tournament=self, participant=p))

        game_count = len(participants) / 2
        participants = list(permutations(participants))[randrange(0, len(participants))]  # randomize participants
        top_half = sorted(participants[:game_count], key=lambda x: x.rating, reverse=True)  # sort each half by rating
        bottom_half = sorted(participants[game_count:], key=lambda x: x.rating, reverse=True)  # before pairings

        for i in range(game_count if game_count * 2 == len(participants) else game_count + 1):
            p1 = top_half[i] if i < len(top_half) else None  # if odd number of players top half < bottom half
            p2 = bottom_half[i]
            game = self.create_game([], no=i + 1, p1=p1, p2=p2)

            if not game.p1:
                game.finish(0, 1)  # player 2 scores a point without playing - gets a BYE!
            else:
                game.save()

        self.save()

    @transaction.atomic
    def advance(self):
        if self.end_date:
            raise Exception('Tournament has ended.')

        # gather players with scores
        all_games = list(self.games.all().select_related('p1', 'p2'))
        round_games = [x for x in all_games if x.round == self.current_round]
        scores, players = self.get_players_and_scores(round_games)

        self.current_round += 1

        # generate pairs and create games
        pairs = self.generate_pairs(players, scores, all_games)
        for i, p in enumerate(pairs):
            p1 = p[0]
            p2 = p[1] if len(p) > 1 else None

            game = self.create_game(all_games, no=i + 1, p1=p1, p2=p2)
            if not p2:
                game.finish(1, 0)
            else:
                game.save()

        self.save()

    # end tournament and apply tie breaking rules if necessary
    @transaction.atomic
    def finish(self):
        if self.current_round < self.rounds:
            raise Exception('There are rounds that are still pending.')

        all_games = list(self.games.all().select_related('p1', 'p2'))
        round_games = [x for x in all_games if x.round == self.current_round]
        scores, players = self.get_players_and_scores(round_games)

        self.end_date = timezone.now()

        finalists = [p for p in players if players[p] == scores[0]]
        if len(finalists) == 1:
            self.winner = finalists[0]
        else:
            self.winner = self.break_tie(all_games, finalists)

        for p in players.keys():
            p.update_rating(self, all_games)
            p.save()

        self.save()
