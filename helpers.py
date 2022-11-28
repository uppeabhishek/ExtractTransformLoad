from requests import post, get, HTTPError

BASE_URL = 'http://localhost:3123/animals/v1'


def retry_request(url, callbacks, errors, request_type='GET', request_body=None):
    while True:
        try:
            if request_type == 'POST':
                request = post(f'{BASE_URL}{url}', json=request_body)
            else:
                request = get(f'{BASE_URL}{url}')

            request.raise_for_status()
            for callback in callbacks:
                callback(request.json())
            break
        except HTTPError as err:
            errors.append(err)
