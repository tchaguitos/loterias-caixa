import urllib
import random
import json

from collections import Counter
from urllib import request
from datetime import date

def get_full_url(url, game, number=None):

    if number:
        full_url = f'{ url }/{ game }/{ number }'

    else:
        full_url = f'{ url }/{ game }'

    return full_url


def get_and_read_response(url):
    req = request.Request(url)
    opener = request.build_opener()
    res = opener.open(req)

    results = json.loads(res.read())

    return results


def parse_resonse(response):
    
    if response:
        parsed = json.loads(response)
        return parsed

    else:
        pass


def get_last_game_results(url):

    results = get_and_read_response(url)

    if not isinstance(results, bool):

        response = {
            'numbers': results['sorteio'],
            'last_game_number': results['numero'],
            'date': results['data']
        }

        return json.dumps(response)


def get_last_to_first_game_results(url, game, number):

    all_results = []

    while number > 0:

        print(f'buscando informações do concurso de número { number } da { game }')

        full_url = get_full_url(url, game, number)

        response_result = get_last_game_results(full_url)
        parsed = parse_resonse(response_result)

        if parsed:
            all_results += parsed['numbers']

        number = number - 1

    return all_results


def get_results(game):

    try:
        file = open(f'{ game }-all-results.txt', 'r')

        last_to_first_games = file.read()
        last_to_first_games = last_to_first_games.split(', ')
    
    except Exception:
        url = 'https://www.lotodicas.com.br/api'

        full_url = get_full_url(url, game)
        response_result = get_last_game_results(full_url)
        parsed = parse_resonse(response_result)

        last_game_number = parsed['last_game_number']
        last_to_first_games = get_last_to_first_game_results(url, game, last_game_number)

        open_or_create_file_and_write_results(game, last_to_first_games, 'all-results')

    return last_to_first_games


def get_most_common(game, result_list, quantity_of_numbers):

    cnt = Counter(result_list)

    most_numbers_frequency = cnt.most_common(quantity_of_numbers)
    numbers_most_sorted = [pair[0] for pair in most_numbers_frequency]

    shuffle_numbers = sorted(numbers_most_sorted, key=lambda k: random.random())
    numbers = sorted(shuffle_numbers, key=lambda k: random.random())

    open_or_create_file_and_write_results(game, numbers, f'{ quantity_of_numbers }-most-common')

    return numbers


def get_games(game, most_common, total_of_games, total_of_numbers_by_game):

    games = []

    init = 0
    last = total_of_numbers_by_game

    limit = (total_of_games*total_of_numbers_by_game+1)

    while(last < limit):

        list_game = list(most_common[init:last])

        list_game.sort()

        games.append(list_game)
        
        init += total_of_numbers_by_game
        last += total_of_numbers_by_game
    
    open_or_create_file_and_write_results(game, games, f'{ total_of_games }-games-{ date.today() }')

    return games

def open_or_create_file_and_write_results(game, result_list, description):
    file = open(f'{ game }-{ description }.txt', 'w')

    file.write(str(result_list))

    file.close()

    return file

result_list = get_results('mega-sena') # lotofacil, mega-sena, quina, dupla-sena, lotomania, dia-de-sorte
most_common = get_most_common('mega-sena', result_list, 24)
games = get_games('mega-sena', most_common, 2, 6)

print(games)
