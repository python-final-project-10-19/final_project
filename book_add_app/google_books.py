import requests


def google_books(query, num_results):
    results = []

    response = requests.get('https://www.googleapis.com/books/v1/volumes?q={}&maxResults={}'.format(query, num_results)).json()
    if 'items' in response:
        results_list = response['items']

        for result in results_list:
            try:
                title = result['volumeInfo']['title']
            except:
                title = ''
            try:
                author = result['volumeInfo']['authors'][0]
            except:
                author = ''
            try:
                description = result['volumeInfo']['description']
            except:
                description = ''
            try:
                categories = result['volumeInfo']['categories']
            except:
                categories = ''
            try:
                image_url = result['volumeInfo']['imageLinks']['thumbnail']
            except:
                image_url = ''

            results.append({
                'title': title,
                'author': author,
                'description': description,
                'categories': categories,
                'image_url': image_url,
                # 'purchase_link': result['saleInfo']['buyLink'],
                })

    return results
