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

    def search(self, minsup):
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
    def test_supermarket(self):
        transactions = [['Bread', 'Milk'], ['Bread', 'Diaper', 'Beer', 'Eggs'], ['Milk', 'Diaper', 'Beer', 'Coke'],
                        ['Bread', 'Milk', 'Diaper', 'Beer'], ['Bread', 'Milk', 'Diaper', 'Coke'],
                        ['RMCF', 'RealMadrid'], ['RealMadrid'], ['RealMadrid'], ['RealMadrid', 'rmalive', 'HalaMadrid'],
                        ['RealMadrid', 'HalaMadrid', 'Neymar'], ['Ajaxbet', 'Barcelona', 'RealMadrid'],
                        ['RealMadrid', 'rmalive', 'HalaMadrid'], ['Futbol', 'RealMadrid'],
                        ['ChampionsLeague', 'LigadosCampe', 'FutebolFeminino', 'FCBarcelona', 'RealMadrid', 'ElCl',
                         'CampNou'], ['RealMadrid', 'SuperCopa'], ['Juventus', 'RealMadrid', 'Pogba', 'Psg'],
                        ['RealMadrid'],
                        ['realmadrid', 'madrid', 'halamadrid', 'halla_m2adrid', 'cristiano', 'benzema', 'zidane',
                         'Ramos', 'explore'], ['RealMadrid', 'FCBarcelona', 'SupercopadeEspa'],
                        ['Ajaxbet', 'Barcelona', 'RealMadrid'], ['Bar', 'RealMadrid', 'Sporting', 'CopaDelRey'],
                        ['Camile', 'Mbapp', 'RealMadrid', 'PSG'],
                        ['HalaMadrid', 'SuperCopa', 'RealFootball', 'RealMadrid', 'SoccerGirl', 'HalaMadridYNadaMas',
                         'MadridistaHastaLaMuerte'], ['RealMadrid', 'MatchWorn', 'Ozil'],
                        ['Supercopa', 'Barcelona', 'RealMadrid'], ['RealMadrid'],
                        ['fcb', 'barcelona', 'xavi', 'koeman', 'madrid', 'realmadrid', 'pique'],
                        ['fcb', 'barcelona', 'xavi', 'koeman', 'madrid', 'realmadrid', 'pique'],
                        ['fcb', 'barcelona', 'xavi', 'koeman', 'madrid', 'realmadrid', 'pique'],
                        ['RealMadrid', 'Haaland', 'mbappe', 'Vinicius'], ['HalaMadrid', 'RealMadrid', 'Sports'],
                        ['RealMadrid', 'Valencia', 'ViniciusJunior'],
                        ['realmadrid', 'madrid', 'halamadrid', 'halla_m2adrid', 'cristiano', 'benzema', 'zidane',
                         'Ramos', 'explore'], ['RealMadrid', 'rmalive', 'HalaMadrid', 'Vinici'],
                        ['RealMadrid', 'Haaland'], ['RealMadrid', 'SuperCopa', 'HalaMadrid'], ['RealMadrid'],
                        ['An', 'VIPDeportivo', 'RealMadrid', 'Vinicius', 'Benzema', 'LaLigaSantander'],
                        ['An', 'VIPDeportivo', 'RealMadrid', 'Vinicius', 'Benzema', 'LaLigaSantander'],
                        ['TiempoExtraRD', 'LionelMessi', 'Messi', 'JerzyDudek', 'Barcelona', 'RealMadrid',
                         'FCBarcelona', 'LeoMessi'], ['RealMadrid'], ['RealMadrid'], ['RealMadrid'], ['RealMadrid'],
                        ['RealMadrid'], ['RealMadrid'],
                        ['RealMadrid', 'HalaMadridYNadaMas', 'marca', 'tv3', 'Barcelona'],
                        ['ACMilan', 'Milan', 'FranckKessie', 'bursatransfer', 'LigaItalia', 'SvenBotman', 'RealMadrid',
                         'Liverpool', 'Tottenham', 'Lille'],
                        ['HalaMadrid', 'RealMadrid', 'HalaMadridYNadaMas', 'SiguemeYTeSigo'],
                        ['TiempoExtraRD', 'LionelMessi', 'Messi', 'JerzyDudek', 'Barcelona', 'RealMadrid',
                         'FCBarcelona', 'LeoMessi'], ['TV3', 'RealMadrid', 'mayorcuetadetontosencatalu'],
                        ['s', 'deportes', 'futbol', 'RealMadrid'], ['RealMadrid', 'SuperCopa'],
                        ['Mbappe', 'PSG', 'RealMadrid'], ['RealMadrid', 'Vinic'], ['RealMadrid'],
                        ['Viniciusjr', 'RealMadrid'], ['RealMadrid', 'Vinicius'],
                        ['Ajaxbet', 'Barcelona', 'RealMadrid'], ['RealMadrid', 'Barcelona', 'ElClasico', 'LaZabawa'],
                        ['RealMadrid'],
                        ['viniciusjr', 'benzema', 'barcellona', 'viniciusjr', 'benzema', 'barcellona', 'RealMadrid',
                         'ligasantander', 'blancos'], ['HalaMadrid', 'RealMadrid'], ['Lunes', 'RealMadrid', 'futbol'],
                        ['RealMadrid', 'Vinicius'], ['RealMadrid', 'Yabusele', 'Deck'], ['Barcelona', 'RealMadrid'],
                        ['RealMadrid', 'Benzema', 'Liga'],
                        ['PapoComTironi', 'ViniciusJr', 'Neymar', 'Tite', 'Sele', 'RealMadrid', 'PSG'],
                        ['Ajaxbet', 'Barcelona', 'RealMadrid'],
                        ['Sevilla', 'Cinco', 'SoyNuevaPrensa', 'RealMadrid', 'Record', 'Deportes', 'F'],
                        ['n00nex', 'HalaMadrid', 'Madridista', 'losblancos', 'VAMOS', 'realmadrid', 'real', 'madrid',
                         'RealMadrid', 'CeferinOut', 'UEFA', 'CeferinShame'],
                        ['Ceballos', 'Ancelotti', 'Supercopa', 'ElClasico', 'RealMadrid'], ['RealMadrid', 'Supercopa'],
                        ['RealMadrid', 'LF'], ['RealMadrid']]

        result = GSP(transactions).search(0.04)

        print("========= Status =========")
        print("Transactions: {}".format(transactions))
        print("GSP: {}".format(result))
