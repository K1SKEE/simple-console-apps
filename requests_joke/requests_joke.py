"""Задачка получить get-запросы по ссылке (библиотека requests)"""
import json
import requests

link = 'https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php'


def pars_link(link, amount_requests):
    count_good_jokes = 0
    count_bad_jokes = 0
    count_save_jokes = 0
    good_joke = []
    jokes = {'data': good_joke}
    for i in range(amount_requests):
        r = requests.get(link)
        if 'код' in r.text.lower() or len(r.text) >= 60:
            count_good_jokes += 1
            good_joke.append({f'joke_{count_good_jokes}': r.text})
            count_save_jokes += 1
        else:
            count_bad_jokes += 1
    amount_requests = {'Количество запросов': amount_requests}
    amount_save_jokes = {'Количество сохраненных шуток': count_save_jokes}
    amount_bad_jokes = {'Количество неудачных шуток': count_bad_jokes}
    amount_good_jokes = {'Количество удачных шуток': count_good_jokes}
    result = [jokes, amount_requests, amount_save_jokes, amount_bad_jokes,
              amount_good_jokes]
    with open('homework.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return result

if __name__=='__main__':
    print(pars_link(link, 100))
    