from collections import Counter

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from challenges.models.challenge import Challenge
from challenges.models.team import Team
from challenges.models.competitor import Competitor


class ChallengeAdmin(admin.ModelAdmin):
    fields = ('endomondo_id',)


class CompetitorForm(forms.ModelForm):

    def _get_first_duplicates(self, counter):
        for item, count in counter.items():
            if count > 1:
                return item
        return None

    def clean(self):
        """
        This is the function that can be used to 
        validate your model data from admin
        """
        super().clean()
        teams = self.cleaned_data.get('teams')

        challenge_ids = Counter([team.challenge.id for team in teams])
        duplicate_id = self._get_first_duplicates(challenge_ids)
        if duplicate_id is not None:
            duplicate_names = [team.name for team in teams if team.challenge.id == duplicate_id]
            duplicate_names_quoted = ['"{}"'.format(name) for name in duplicate_names]
            duplicate_names_str = ', '.join(duplicate_names_quoted)
            raise ValidationError('The following teams are in the same challenge: {}'.format(duplicate_names_str))


class CompetitorAdmin(admin.ModelAdmin):
    fields = ('endomondo_id', 'display_name', 'teams')
    form = CompetitorForm


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Team)
admin.site.register(Competitor, CompetitorAdmin)