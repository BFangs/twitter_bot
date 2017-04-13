"""Generate markov text from text files."""


from random import choice, shuffle
import sys

#modules required for tweeting function
import os
import twitter

def open_and_read_file(paths):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    text = ""
    for path in paths:
        contents1 = open(path)
        # contents2 = open(file_path2)
        text = text + contents1.read()
        contents1.close()

    return text



def make_chains(text_string, n):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
    """

    chains = {}
    words = text_string.split()
    shuffle(words)
    # looping over indices up to 3rd from n so every bigram can have a value
    # bigrams are put in dictionary called chains
    for i in range(len(words)-n):
        #bigram = (words[i], words[i+1])
        ngram = words[i:i+n]
        ngram = tuple(ngram)
        if chains.get(ngram):
            chains[ngram].append(words[i+n])
        else:
            chains[ngram] = [words[i+n]]
    return chains


def get_capitalized(chains):
    """when we need a capitalized letter start
    """
    while True:
        ngram = choice(chains.keys())
        random_thing = choice(chains[ngram])
        if random_thing[0].isupper():
            return random_thing
        else:
            continue

def make_text(chains, n):
    """Returns text from chains."""

    words = []

    counter = 0
    while counter < 130:
        ngram = choice(chains.keys())
        if chains.get(ngram):
            #link = bigram[0], bigram[1], random_thing
            if counter == 0 or words[-1][-1] == "?":
                random_thing = get_capitalized(chains)
                #print random_thing
            else:
                random_thing = choice(chains[ngram])
            words.append(random_thing)
            #print words
            counter = counter + len(random_thing) + 1
            ngram = [ngram[x] for x in range(1, n)] + [random_thing]
            ngram = tuple(ngram)
            #bigram = (bigram[-1], random_thing)
        else:
            break
    #return words
    return " ".join(words)



def tweet(to_tweet):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    # status = api.PostUpdate(to_tweet)
    # print status.text

    trend_list = api.GetTrendsWoeid(woeid= 1)
    our_hashtag = choice(trend_list)
    print type(our_hashtag)
    print our_hashtag




n = int(sys.argv[1])

path_list = sys.argv[2:]


# Open the file and turn it into one long string
input_text = open_and_read_file(path_list)

# Get a Markov chain
chains = make_chains(input_text, n)

# Produce random text
random_text = make_text(chains, n)



tweet(random_text)
