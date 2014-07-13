from math import sqrt


def similarity_using_pearson(preferences, p1, p2):
    common_items = {}
    for item in preferences[p1]:
        if item in preferences[p2]:
            common_items[item] = 1

    number_of_common_items = len(common_items)

    if number_of_common_items == 0: return 0;

    # adds up all of the scores that have been made for the common items for each person
    sum_of_scores_for_p1 = sum([preferences[p1][item] for item in common_items])
    sum_of_scores_for_p2 = sum([preferences[p2][item] for item in common_items])

    # adds up the squares of each scores for each person,
    sum_of_squared_scores_for_p1 = sum([pow(preferences[p1][item], 2) for item in common_items])
    sum_of_squared_scores_for_p2 = sum([pow(preferences[p2][item], 2) for item in common_items])

    # sum of the products
    sum_of_products = sum([preferences[p1][item] * preferences[p2][item] for item in common_items])

    numerator = sum_of_products - (sum_of_scores_for_p1 * sum_of_scores_for_p2 / number_of_common_items)
    denominator = sqrt((sum_of_squared_scores_for_p1 - pow(sum_of_scores_for_p1, 2) / number_of_common_items)
                       * (sum_of_squared_scores_for_p2 - pow(sum_of_scores_for_p2, 2) / number_of_common_items))
    if denominator == 0: return 0

    return numerator / denominator


def get_recommendations(preferences, person_to_find_recommendations_for, similarity=similarity_using_pearson):
    totals = {}
    total_similarity_score = {}

    for person in preferences:
        if person == person_to_find_recommendations_for: continue
        similarity_score = similarity(preferences, person_to_find_recommendations_for, person)

        if similarity_score <= 0:
            continue

        for item in preferences[person]:
            if item not in preferences[person_to_find_recommendations_for] or \
                            preferences[person_to_find_recommendations_for][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += preferences[person][item] * similarity_score

                total_similarity_score.setdefault(item, 0)
                total_similarity_score[item] += similarity_score

    rankings = [(total / total_similarity_score[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


def transform_preferences(preferences):
    result = {}

    for person in preferences:
        for item in preferences[person]:
            result.setdefault(item, {})

            result[item][person] = preferences[person][item]
    return result


def top_matches(preferences, person, number_of_recommendations=5, similarity=similarity_using_pearson):
    scores = [(similarity(preferences, person, other), other) for other in preferences if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:number_of_recommendations]


def calculate_similar_items(preferences, number_of_recommendations=10):
    result = {}

    item_preferences = transform_preferences(preferences)

    for item in item_preferences:
        scores = top_matches(item_preferences, item, number_of_recommendations=number_of_recommendations)
        result[item] = scores
    return result


def get_recommended_items(preferences, item_match, user):
    user_ratings = preferences[user]
    scores = {}
    total_similarity_scores = {}

    #loop over items rated by user
    for item, rating in user_ratings.items():

        #loop over items similar to this item
        for similarity, similar_item in item_match[item]:

            if similar_item in user_ratings:
                continue

            scores.setdefault(similar_item,0)
            scores[similar_item]+=similarity*rating

            total_similarity_scores.setdefault(similar_item,0)
            total_similarity_scores[similar_item]+=similarity

    rankings=[(score/total_similarity_scores[item],item) for item,score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings




