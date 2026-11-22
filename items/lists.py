"""The lists a space keeps, one per kind of game, as shown in the tabs of "Our lists"."""

from dataclasses import dataclass
from typing import Callable

from . import builtins
from .models import BuiltIn


@dataclass(frozen=True)
class GameList:
    slug: str
    name: str
    # The page that shows it, as an "items:" URL name.
    url_name: str
    played_with: str
    # What one entry is called, and several.
    one: str
    many: str
    # Each takes a space: how many entries it has, and emptying it.
    count: Callable
    clear: Callable
    # The kinds of built-in entries "Generate a list" fills it with (BuiltIn.kind).
    kinds: tuple
    # Its tab on the Built-in lists page.
    built_in_tab: str

    def describe(self, count):
        return f"{count} {self.one if count == 1 else self.many}"

    def ours(self):
        """How many entries "Generate a list" has to offer in all."""
        return BuiltIn.objects.filter(kind__in=self.kinds).count()

    def missing(self, space):
        """How many of ours the space's list doesn't have."""
        return sum(len(builtins.missing(space, kind)) for kind in self.kinds)

    def generate(self, space, user=None):
        """Add whatever of ours the list is missing. Returns how many were added."""
        return sum(builtins.add_missing(space, kind, user) for kind in self.kinds)


def _clear_kinky_list(space):
    # Deleting wishes cascades to their assignments; drop the now-empty game sessions too.
    space.items.all().delete()
    space.categories.all().delete()
    space.game_sessions.all().delete()


def _clear_truth_or_dare(space):
    space.truths.all().delete()
    space.dares.all().delete()


KINKY_LIST = GameList(
    slug="kinky-list",
    name="The Kinky List",
    url_name="list",
    played_with="Kinky List: Randomize, Pick your favorite, Just ask! and Try new things!",
    one="wish",
    many="wishes",
    count=lambda space: space.items.count(),
    clear=_clear_kinky_list,
    kinds=(BuiltIn.WISH,),
    built_in_tab="wishes",
)

TRUTH_OR_DARE = GameList(
    slug="truth-or-dare",
    name="Truth or Dare",
    url_name="truth_or_dare",
    played_with="Truth or Dare",
    one="truth or dare",
    many="truths and dares",
    count=lambda space: space.truths.count() + space.dares.count(),
    clear=_clear_truth_or_dare,
    kinds=(BuiltIn.TRUTH, BuiltIn.DARE),
    built_in_tab="truths",
)

WOULD_YOU_RATHER = GameList(
    slug="would-you-rather",
    name="Would you rather",
    url_name="would_you_rather",
    played_with="Would you rather",
    one="question",
    many="questions",
    count=lambda space: space.questions.count(),
    clear=lambda space: space.questions.all().delete(),
    kinds=(BuiltIn.QUESTION,),
    built_in_tab="questions",
)

LISTS = {game_list.slug: game_list for game_list in (KINKY_LIST, TRUTH_OR_DARE, WOULD_YOU_RATHER)}
