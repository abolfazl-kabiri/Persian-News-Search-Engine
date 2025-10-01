import re


def convert_numbers(text):
    english_numbers = "0123456789"
    persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
    normal_text = text.translate(text.maketrans(english_numbers, persian_numbers))
    return normal_text


def apply_patterns_replacement(patterns, text):
    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)
    return text


def replace_unicode_symbols(text):
    replacements = [
        ("﷽ ", "بسم الله الرحمن الرحیم"),
        ("﷼", "ریال"),
        ("(ﷰ|ﷹ)", "صلی"),
        ("ﷲ", "الله"),
        ("ﷳ", "اکبر"),
        ("ﷴ", "محمد"),
        ("ﷵ", "صلعم"),
        ("ﷶ", "رسول"),
        ("ﷷ", "علیه"),
        ("ﷸ", "وسلم"),
        ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
        ("آ", "ا"),
        ("ك", "ک"),
        ("ي", "ی"),
    ]
    text = apply_patterns_replacement(replacements, text)
    return text


def adjust_spacing(text):
    rules = [
        (r"([^ ]ه) ی ", r"\1‌ی "),
        (r"(^| )(ن?می) ", r"\1\2"),
        (
            r"(?<=[^\n\d "
            + r"\.:!،؛؟»\]\)\}"
            + r"]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
            + r"\.:!،؛؟»\]\)\}"
            + r"]|$)",
            r"\1"
        ),
        (
            r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + r"\.:!،؛؟»\]\)\}"
            + "]|$)",
            r"\1\2"
        ),
        ("(ه)(ها)", r"\1\2"),
    ]

    text = apply_patterns_replacement(rules, text)
    return text


def normalize(text):
    text = replace_unicode_symbols(text)
    text = adjust_spacing(text)
    text = convert_numbers(text)
    return text


def tokenize(text):
    pattern = re.compile(r'([؟!?]+|[\d.:]+|[:.،؛»\])}"«\[({/\\])')
    text = pattern.sub(r" \1 ", text.replace("\n", " ").replace("\t", " "))

    punctuations = [')', '(', '>', '<', "؛", "،", '{', '}', "؟", ':', "–", '»', '"', '«', '[', ']', '"', '+', '=', '?',
                    '/', '//', '\\', '|', '!', '%', '&', '*', '$', '#', '؟', '.', '_', '', 'EMAIL', 'LINK', 'ID', 'NUM',
                    'NUMF', ' ', '-']

    tokens = [word for word in text.split(" ") if word and word not in punctuations]
    return tokens


def process_verbs(tokens):
    before_verbs = {
        "خواهم",
        "خواهی",
        "خواهد",
        "خواهیم",
        "خواهید",
        "خواهند",
        "نخواهم",
        "نخواهی",
        "نخواهد",
        "نخواهیم",
        "نخواهید",
        "نخواهند",
    }

    if len(tokens) == 1:
        return tokens

    result = [""]
    for token in reversed(tokens):
        if token in before_verbs:
            result[-1] = token + "_" + result[-1]
        else:
            result.append(token)
    return list(reversed(result[1:]))



class Posting:
    def __init__(self):
        self.frequency = 0
        self.positions = []
        self.tf_idf = 0

    def __str__(self):
        return f"frequency: {self.frequency} , tf_idf: {self.tf_idf},positions: {self.positions}"


class PostingsList:
    def __init__(self):
        self.frequency = 0
        self.postings = {}

    def __str__(self):
        return f"frequency: {self.frequency} ,postings: {self.postings}"
