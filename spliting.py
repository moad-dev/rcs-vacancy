import re
from razdel import sentenize


def split_list_merge_by_pattern(lst: list, pattern: str) -> list[str]:
    result = []
    for token in lst:
        token = token.replace('&quot;', '"')
        regular_splited = re.split(pattern, token)
        regular_splited = [text.strip() for text in regular_splited]
        regular_splited = list(filter(None, regular_splited))
        result += regular_splited
    return result


def split(string_to_split: str) -> list[str]:
    sentence_splited = [sentence.text for sentence in sentenize(string_to_split)]
    # |(?<=[а-я]):
    # |(?= [А-Я][а-я])
    # |; +-|; +—|•|; +~|; +\+|—|-
    regular_splited = split_list_merge_by_pattern(sentence_splited, '; +-|; +—|; +~|; +\+|(?<=[а-я]):|\n|•|·|—|⠇|°|⠂|;')
    return regular_splited
