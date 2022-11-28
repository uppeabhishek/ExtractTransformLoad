from copy import copy
from datetime import datetime

from helpers import retry_request


class ExtractTransformLoad:
    """
    The class ExtractTransformLoad performs the following core operations

    1. Get animals using "/animals/v1/animals" endpoint
    2. Get animal json response using "/animals/v1/animals/<id>" endpoint
    3. Transform the "animal" response
    4. Load all the animals into home using "/animals/v1/home"

    The server can sometimes return 5xx response or the server can even pause in some instance. To handle such cases,
    retry mechanism is used where until 2xx response is not received the endpoint gets retried.
    """
    def __init__(self):
        self.current_page = 1
        self.total_pages = None

        self.total_animals = 0
        self.animals_home_post_limit = 100

        self.transformed_animals = []
        self.error_logs = []

    @staticmethod
    def log_animals_home_response(response):
        # currently using print method, can be replaced with proper logging mechanism.
        print(response)

    @staticmethod
    def transform_animal_result(result):
        current_result = copy(result)
        current_result['friends'] = current_result['friends'].split(",")
        if current_result['born_at'] is not None:
            current_result['born_at'] = str(datetime.utcfromtimestamp(current_result['born_at'] / 1000.0))
        return current_result

    def add_to_result(self, result):
        self.transformed_animals.append(self.transform_animal_result(result))
        if len(self.transformed_animals) == self.animals_home_post_limit:
            self.post_to_animals_home()
            self.transformed_animals = []

    def set_page_details(self, animal):
        self.current_page = self.current_page + 1
        self.total_animals += len(animal['items'])
        self.total_pages = animal['total_pages']

    def post_to_animals_home(self):
        retry_request('/home', [self.log_animals_home_response], self.error_logs, 'POST', self.transformed_animals)

    def get_animal(self, animals):
        for animal in animals['items']:
            retry_request(f'/animals/{animal["id"]}', [self.add_to_result], self.error_logs, )

    def get_animals(self):
        while self.total_pages is None:
            retry_request('/animals', [self.set_page_details, self.get_animal], self.error_logs)

        while self.total_pages is not None and self.current_page <= self.total_pages:
            retry_request(f'/animals/?page={self.current_page}', [self.set_page_details, self.get_animal],
                          self.error_logs)

        # post the remaining animals to animals home
        if len(self.transformed_animals):
            self.post_to_animals_home()
            self.transformed_animals = []


if __name__ == '__main__':
    e = ExtractTransformLoad()
    e.get_animals()
