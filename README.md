ExtractTransformLoad

<li>The purpose of the project is to extract animals data, transform the data and load the output
into animals home.</li>


Installation Steps

1. Download the Docker image:
   https://storage.googleapis.com/lp-dev-hiring/images/lp-programming-challenge-1-1625758668.tar.gz
2. Load the container: `docker load -i lp-programming-challenge-1-1625758668.tar.gz`.
3. Run `docker run --rm -p 3123:3123 -ti lp-programming-challenge-1`
4. Open `http://localhost:3123/` to check if the server is running.
5. Run the command `docker run abhishekuppe/leadpages`


The output will be printed after all the animals are loaded into "/animals/v1/home". It takes 
a couple of minutes to load all the animals.