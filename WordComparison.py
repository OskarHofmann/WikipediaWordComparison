import wikipedia
import re
import string


wikipedia.set_lang("de")

# most common German words to filter out later (if needed replace with available list of other language)
top_100_plus_german = {'während', 'davon', 'insbesondere', 'zahlreichen', 'sowie', 'bezeichnet', 'bzw', 'einiger', 'damit', 'daher', 'beim', 'denen', 'jedoch', 'dieses', 'anderen', 'wieder', 'von', 'eine', 'war', 'kann', 'ist', 'auch', 'dann', 'über', 'sie', 'die', 'sei', 'das', 'ich', 'der', 'durch', 'so', 'gegen', 'hat', 'millionen', 'ihre', 'und', 'aus', 'noch', 'sein', 'mit', 'werden', 'hatte', 'dass', 'haben', 'oder', 'dem', 'unter', 'immer', 'aber', 'ein', 'prozent',
                       'soll', 'Es', 'als', 'für', 'einer', 'einem', 'wird', 'seine', 'zum', 'will', 'bis', 'vom', 'des', 'nur', 'wenn', 'am', 'um', 'sie', 'ein', 'er', 'vor', 'jahren', 'sagte', 'zu', 'das', 'nicht', 'bei', 'und', 'es', 'habe', 'nach', 'Uhr', 'jahr', 'In', 'was', 'wurde', 'zwei', 'eines', 'wie', 'im', 'euro', 'in', 'einen', 'sich', 'worden', 'keine', 'an', 'seiner', 'zur', 'der', 'wir', 'schon', 'im', 'zwischen', 'die', 'diese', 'mehr', 'auf', 'den', 'dieser', 'können', 'man', 'sind'}

# words to find commonalities for
words = ["Madrid", "Winterruhe"]


wiki_pages = []
unique_words = []

# try to find Wikipedia page for each word and add its content to the list
try:
    for idx, wort in enumerate(words):
        # auto_suggest may suggest other pages even though page for that exact word exist
        wiki_pages.append(wikipedia.page(wort, auto_suggest=False).content)
except wikipedia.exceptions.DisambiguationError as e:
    print(e.options)
    exit()


for page in wiki_pages:
    # filter out headers as indicated by 2-4 surrounding equal signs as certain headers are very common without showing an actual commonality
    text = re.sub('={2,4}.*?={2,4}', '', page) # =(2-4 times) + lazy (non-greedy) match for any group characters + =(2-4 times)

    # convert hpyhens to spaces as punctuation is removed in the next step to maintain meaning of words seperated by hyphens
    text = re.sub('-', ' ', text)

    # remove punctuation as we only want to look for actual words
    text = text.translate(str.maketrans('', '', string.punctuation))

    # make a set of all words in the remaining text and add it to the list of unique words for each article
    unique_words.append(set(text.lower().split()))

#find the words that appear in all the selected Wikipedia pages
common_words = unique_words[0]
for word in unique_words[1:]:
    common_words = common_words.intersection(word)

#remove the most common words in your language as they do not really show a commonality
common_without_top100 = common_words.difference(top_100_plus_german)
print("Commong words:")
print(common_without_top100)


# print each line in the Wikipedia articles that contain the common words to check/understand commonalityies
for wort in common_without_top100:
    print(wort)
    for page in wiki_pages:
        for line in page.splitlines():
            if wort in line.lower():
                print(line)
