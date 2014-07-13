import os
import pickle
from unittest import TestCase
from recommendor_engine.src.recommendor import transform_preferences, calculate_similar_items, get_recommended_items

__author__ = 'Chris'

critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


class TestTransformPreferences(TestCase):
    def test_should_transform_preferences(self):
        prefs = {'somePerson': {'someItem': 2.5, 'someOtherItem': 3.5}}

        transformed_prefs = transform_preferences(prefs)
        self.assertEqual(transformed_prefs['someItem']['somePerson'], 2.5)


    def test_should_recommend_items(self):
        similar_items = calculate_similar_items(critics)

        recommended_items= get_recommended_items(critics, similar_items, 'Toby')
        self.assertEqual(recommended_items[0][1],'Lady in the Water')

    def test_pickle(self):
        similar_items = calculate_similar_items(critics)
        pickled_data = 'similar_items.dat'
        pickle.dump(similar_items,open(pickled_data,'wb'))
        pickled_similar_items = pickle.load(open(pickled_data,'rb'))
        self.assertEqual(similar_items,pickled_similar_items)

        os.remove(pickled_data)