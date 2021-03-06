from collections import defaultdict
from itertools import chain
from typing import Dict, Iterable, List, NewType, Tuple

import dawg
from utils.cree_lev_dist import remove_cree_diacritics

# A simplified form intended to be used within the affix search trie.
SimplifiedForm = NewType("SimplifiedForm", str)


class AffixSearcher:
    """
    Enables prefix and suffix searches given a list of words and their wordform IDs.
    """

    # TODO: "int" should be Wordform PK type

    def __init__(self, words: Iterable[Tuple[str, int]]):
        self.text_to_ids: Dict[str, List[int]] = defaultdict(list)

        words_marked_for_indexing = [
            (simplified_text, wordform_id)
            for raw_text, wordform_id in words
            if (simplified_text := self.to_simplified_form(raw_text))
        ]

        for text, wordform_id in words_marked_for_indexing:
            self.text_to_ids[self.to_simplified_form(text)].append(wordform_id)

        self._prefixes = dawg.CompletionDAWG(
            [text for text, _ in words_marked_for_indexing]
        )
        self._suffixes = dawg.CompletionDAWG(
            [_reverse(text) for text, _ in words_marked_for_indexing]
        )

    def search_by_prefix(self, prefix: str) -> Iterable[int]:
        """
        :return: an iterable of Wordform IDs that match the prefix
        """
        term = self.to_simplified_form(prefix)
        matched_words = self._prefixes.keys(term)
        return chain.from_iterable(self.text_to_ids[t] for t in matched_words)

    def search_by_suffix(self, suffix: str) -> Iterable[int]:
        """
        :return: an iterable of Wordform IDs that match the suffix
        """
        term = self.to_simplified_form(suffix)
        matched_reversed_words = self._suffixes.keys(_reverse(term))
        return chain.from_iterable(
            self.text_to_ids[_reverse(t)] for t in matched_reversed_words
        )

    @staticmethod
    def to_simplified_form(query: str) -> SimplifiedForm:
        """
        Convert to a simplified form of the word and its orthography to facilitate affix
        search.  You SHOULD throw out diacritics, choose a Unicode Normalization form,
        and choose a single letter case here!
        """
        # TODO: make this work for not just Cree!
        # TODO: allow users to override this method
        return SimplifiedForm(remove_cree_diacritics(query.lower()))


def _reverse(text: SimplifiedForm) -> SimplifiedForm:
    return SimplifiedForm(text[::-1])
