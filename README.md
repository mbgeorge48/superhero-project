# Superhero Project

This is a lightweight app for rendering superhero information using data fetched from https://superheroapi.com/. The service connects to superheroapi using an env var in `.env` called `SUPERHERO_API_TOKEN`, ensure to head to their homepage to generate your own token before you run the service.

When the server initialises it uses **BeautifulSoup** to scrape all the hero IDs from https://superheroapi.com/ids.html, this is because there's no list endpoint available and rather than individually fetching heroes one by one, we build a list of hero names and IDs that we can hydrate on a case by case basis.

It uses a simple python dictionary to act as a caching layer to avoid repetitive API calls and by using a python dictionary we know that fetching information from the cache will be lightning fast.

There is a **Pydantic** data layer to ensure data we fetch fits into the correct shape, it also allows us to transform some data. i.e. the image url gets changed once we've fetched the information from the API. As a side note not every hero has a complete data set, rather than changing the data we recieve we handle that in the Jinja template.

Using **FastAPI** and **Jinja2** to handle requests and server-side rendering to keep requests performant, simple and fast.

**Most common tasks can be carried out using the scripts in the scripts directory**

## Running the scripts

_Note these are design to work on OSX so may need tweaking for other operating systems._

### Setup

**How to run**

```
scripts/setup
```

Once you have run the setup script you will need to go to https://superheroapi.com/ to finish setting up, from there you wil have to create your Superhero API token

### Running the server

**How to run**

```
scripts/server
```

This is a FastAPI service running using Uvicorn. When the service is running locally you can access it through your browser by going to http://127.0.0.1:8000

### Formatting and Testing

**How to run**

```
scripts/format
scripts/test
```

We're using the following libraries for running tests and ensuring a consistent code format is kept.

- **Black**: Uncompromising code formatting.
- **Isort**: Automated import sorting.
- **Flake8**: PEP8 compliance and bug detection.
- **Pytest-asyncio**: Handling asynchronous unit tests for our services and routes.

Tests are localised to test folders colocated with the files they are testing, this keeps unit tests targeted and modular.

## Future iterations

Given more time I'd consider the following features

- Build a more resilient caching solution
    - At the moment when the service restarts the cache gets wiped. Something like Redis would help us here as it moves the cache outside the Uvicorn service which protects it and allows other server instances use it.
- Build a search component
    - The super hero API has the ability to be searched, it would be fun to make use of that to allow the user to search through all 731 heroes for their favourite.
- Rate limiting
    - If we hosted this in a production enviroment we might want to consider rate limiting our server to protect the service from being bombarded with requests.
    - We should also consider the fact we're fetching data from another API, to handle this gracefully we should implment exponential backoff to throttle requests to SuperHeroAPI.
