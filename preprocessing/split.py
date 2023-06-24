import re
from razdel import sentenize

def split_str_with_razdel(string_to_split: str):
    return [sentence.text for sentence in sentenize(string_to_split)]

def split_list_merge_by_pattern(lst: list, pattern: str):
    result = []
    for token in lst:
        regular_splited = re.split(pattern, token)
        regular_splited = list(filter(None, regular_splited))
        result += [text.strip() for text in regular_splited]
    return result

def split(string_to_split: str):
    sentence_splited = split_str_with_razdel(string_to_split)
    regular_splited = split_list_merge_by_pattern(sentence_splited, '\n|(?<=[а-я]):')
    return regular_splited

#
# TEST
#
#splited = re.split('; +-|; +—|•|; +~|; +\+|—|-\n', string_to_split)

def test():
    file = open('data/split_test.txt',mode='r')
    string_to_split = file.read()
    file.close()
    test = split(string_to_split)
    for token in test:
        print(token+"$")

if __name__ == "__main__":
    test()
