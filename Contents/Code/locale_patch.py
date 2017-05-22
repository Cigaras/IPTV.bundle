# -*- coding: utf-8 -*-
"""
    Localization patch for Plex Media Server channels
    https://bitbucket.org/czukowski/plex-locale-patch/
    Copyright: 2015, Korney Czukowski
    License: MIT
"""

languages = list()


# Translate function override to avoid unicode decoding bug.
def L(string):
    initialize_locale()
    local_string = Locale.LocalString(string)
    return str(local_string).decode()


def SetAvailableLanguages(list):
    global languages
    languages = list


# Client language detection.
# Make sure this function does its thing only the first time it's called (once per request).
def initialize_locale():
    if 'Plex-Locale-Patch' in Request.Headers:
        return
    for parse_func in [parse_x_plex_language_value, parse_accept_language_value]:
        value = parse_func()
        if value:
            set_language_header(value)
            break
    if not value:
        Log('Locale Patch: language not detected. All request headers: %s' % str(Request.Headers))
    Request.Headers['Plex-Locale-Patch'] = 'y'


# Parse 'X-Plex-Language' header
def parse_x_plex_language_value():
    if 'X-Plex-Language' in Request.Headers:
        header_value = Request.Headers['X-Plex-Language']
        matched_value = Locale.Language.Match(header_value)
        if matched_value == 'xx':
            return
        Log('Locale Patch: found language in X-Plex-Language header ("%s" matched to "%s")' % (header_value, matched_value))
        return select_available_language([matched_value])


# Parse 'Accept-Language' header
# Based on http://stackoverflow.com/a/17911139
def parse_accept_language_value():
    if 'Accept-Language' in Request.Headers:
        header_value = Request.Headers['Accept-Language']
        # Extract all locales and their preference (q)
        locales = []  # e.g. [('es', 1.0), ('en-US', 0.8), ('en', 0.6)]
        for locale_str in header_value.replace(' ', '').lower().split(','):
            locale_parts = locale_str.split(';q=')
            locale = locale_parts[0]
            if len(locale_parts) > 1:
                locale_q = float(locale_parts[1])
            else:
                locale_q = 1.0
            locales.append((locale, locale_q))
        # Sort locales according to preference
        locales.sort(key=lambda locale_tuple: locale_tuple[1], reverse=True)
        # Remove weights from the list, keep only locale names
        locales = map(lambda locale_tuple: locale_tuple[0], locales)
        if len(locales):
            Log('Locale Patch: found languages in Accept-Language header (%s)' % header_value)
            return select_available_language(locales)


def select_available_language(locales):
    global languages
    if not len(languages):
        Log('Locale Patch: no known available languages, using "%s" as the %s choise. Call SetAvailableLanguages(list) function to improve this.' % (locales[0], 'only' if len(languages) == 1 else 'first'))
        return locales[0]
    for item in locales:
        if item in languages:
            Log('Locale Patch: using available language "%s".' % item)
            return item
    Log('Locale Patch: none of the languages matched available languages.')


def set_language_header(value):
    Request.Headers['X-Plex-Language'] = value