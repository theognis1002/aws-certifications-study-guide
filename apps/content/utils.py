import requests
from django.core.cache import cache
from django.core.exceptions import ValidationError


def clean_text(text):
    """util to clean and properly format text in submitted service description"""
    words = [word.replace("\n", "").strip() for word in text.split()]
    words[0] = words[0].title()
    text = " ".join(words)
    text = text + "." if text[-1] != "." else text
    return text


def detect_profanity(user_text):
    """
    - returns True if profanity detected in user submitted string
    - profanity list is cached for 24 hrs
    """
    cached_profanity_list = cache.get("profanity_list")
    if cached_profanity_list:
        # using cache
        curse_words = cached_profanity_list
    else:
        # setting cache
        curse_words = requests.get(
            "https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt"
        ).text.splitlines()
        cache.set("profanity_list", curse_words, 60 * 60 * 24)

    user_text = "".join(letter.lower() for letter in user_text if letter.isalnum())
    contains_profanity = any(
        [curse_word for curse_word in curse_words if curse_word in user_text]
    )
    return contains_profanity


class ProfanityFilter:
    """
    Custom mixin that detects profanity within user submitted forms.
    Must include list of `user_text_fields`
    """

    def clean(self):
        assert self.user_text_fields
        cleaned_data = super().clean()
        errors = {}
        for field_name in self.user_text_fields:
            if detect_profanity(cleaned_data[field_name]):
                errors[
                    field_name
                ] = "Profanity detected. Please remove all inappropriate language."
        if errors:
            raise ValidationError(errors)
