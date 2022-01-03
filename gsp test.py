
"""
===============================================
GSP (Generalized Sequential Pattern) algorithm
===============================================

GSP algorithm made with Python3 to deal with arrays as transactions.

Example:

transactions = [
                ['Bread', 'Milk'],
                ['Bread', 'Diaper', 'Beer', 'Eggs'],
                ['Milk', 'Diaper', 'Beer', 'Coke'],
                ['Bread', 'Milk', 'Diaper', 'Beer'],
                ['Bread', 'Milk', 'Diaper', 'Coke']
            ]
"""
import tweepy as tw
import logging
from unittest import TestCase
from itertools import product
import multiprocessing as mp
from collections import Counter
from itertools import chain
import numpy as np

logging.basicConfig(level=logging.DEBUG)


class GSP:
    def __init__(self, raw_transactions):
        self.freq_patterns = []
        self._pre_processing(raw_transactions)

    def _pre_processing(self, raw_transactions):
        """Prepare the data

        Parameters:
                raw_transactions: the data that it will be analysed"""

        self.max_size = max([len(item) for item in raw_transactions])
        self.transactions = [tuple(list(i)) for i in raw_transactions]
        counts = Counter(chain.from_iterable(raw_transactions))
        self.unique_candidates = [tuple([k]) for k, c in counts.items()]

    def _is_slice_in_list(self, s, l):
        len_s = len(s)  # so we don't recompute length of s on every iteration
        return any(s == l[i:len_s + i] for i in range(len(l) - len_s + 1))

    def _calc_frequency(self, results, item, minsup):
        # The number of times the item appears in the transactions
        frequency = len(
            [t for t in self.transactions if self._is_slice_in_list(item, t)])
        if frequency >= minsup:
            results[item] = frequency
        return results

    def _support(self, items, minsup=0):
        """ The support count (or simply support) for a sequence is defined as
        the fraction of total data-sequences that "contain" this sequence.
        (Although the word "contains" is not strictly accurate once we
        incorporate taxonomies, it captures the spirt of when a data-sequence
        contributes to the support of a sequential pattern.)

        Parameters
                items: set of items that will be evaluated
                minsup: minimum support"""
        results = mp.Manager().dict()
        pool = mp.Pool(processes=mp.cpu_count())

        for item in items:
            pool.apply_async(self._calc_frequency,
                             args=(results, item, minsup))
        pool.close()
        pool.join()

        return dict(results)

    def _print_status(self, run, candidates):
        logging.debug("""
        Run {}
        There are {} candidates.
        The candidates have been filtered down to {}.\n"""
                      .format(run,
                              len(candidates),
                              len(self.freq_patterns[run - 1])))

    def search(self, minsup=0.2):
        """Run GSP mining algorithm

        Parameters
                minsup: minimum support"""
        assert (0.0 < minsup) and (minsup <= 1.0)
        minsup = len(self.transactions) * minsup

        # the set of frequent 1-sequence: all singleton sequences
        # (k-itemsets/k-sequence = 1) - Initially, every item in DB is a
        # candidate
        candidates = self.unique_candidates

        # scan transactions to collect support count for each candidate
        # sequence & filter
        self.freq_patterns.append(self._support(candidates, minsup))

        # (k-itemsets/k-sequence = 1)
        k_items = 1

        self._print_status(k_items, candidates)

        # repeat until no frequent sequence or no candidate can be found
        while len(self.freq_patterns[k_items - 1]) and (k_items + 1 <= self.max_size):
            k_items += 1

            # Generate candidate sets Ck (set of candidate k-sequences) -
            # generate new candidates from the last "best" candidates filtered
            # by minimum support
            items = np.unique(
                list(set(self.freq_patterns[k_items - 2].keys())))

            candidates = list(product(items, repeat=k_items))

            # candidate pruning - eliminates candidates who are not potentially
            # frequent (using support as threshold)
            self.freq_patterns.append(self._support(candidates, minsup))

            self._print_status(k_items, candidates)
        return self.freq_patterns[:-1]

class gsptest(TestCase):
    def gsp_algorithm(self):
        consumer_key = '00uoWhWMhHFv3VvLmRS92wGss'
        consumer_secret = 'rSsAQhOO2SZ6QNDXS1D6gIkrzuAD4OJ545xnqDlnM6KhVIR7Uj'
        access_token = '1477363091646132228-f3eIclo5ERWkZ0hC7ldO5ISncMmMBR'
        access_token_secret = 'rqvmXTHyQHLprD17WzUDIHjTbQrWVuDV8d73JnY4xJUVg'
        # authenticate
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        search_query = "#RealMadridFutbolClub -filter:retweets"

        # get tweets from the API
        tweets = tw.Cursor(api.search_tweets, q=search_query, lang="es").items(5000)
        # store the API responses in a list
        tweets_copy = []
        for tweet in tweets:
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
            tweets_copy.append(text)

        print("Total Tweets fetched:", len(tweets_copy))
        transactions = [
            ['Bread', 'Milk'],
            ['Bread', 'Diaper', 'Beer', 'Eggs'],
            ['Milk', 'Diaper', 'Beer', 'Coke'],
            ['Bread', 'Milk', 'Diaper', 'Beer'],
            ['Bread', 'Milk', 'Diaper', 'Coke']
        ]

        result = GSP(transactions).search(0.3)

        print("========= Status =========")
        print("Transactions: {}".format(transactions))
        print("GSP: {}".format(result))