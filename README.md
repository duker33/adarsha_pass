[![Hits-of-Code](https://hitsofcode.com/github/duker33/adarsha_pass)](https://hitsofcode.com/view/github/duker33/adarsha_pass)
[![PDD status](http://www.0pdd.com/svg?name=duker33/adarsha_pass)](http://www.0pdd.com/p?name=duker33/adarsha_pass)

# Bot to order passes to Adarsha org

Bot orders passes throw [iq-park](http://iqpark-msk.ru/) business centre to [Adarsha organization](https://vk.com/adarsha_yoga) based in Moscow, Russia.

It's not open source project, since it's not possible to reuse it. But it's open code one.

## Contribution
We appreciate contributions.
In case of implementing features we recommend
to spend not more time then estimated (see the tag with estimate).
For example instead of spending 10 hours please spend just 1 hour
and append subtasks right to the code in [this format](https://github.com/yegor256/pdd#how-to-format).
This method is called Puzzle Driven Development (PDD).
See [short PDD concept description](https://www.yegor256.com/2010/03/04/pdd.html)
to get familiar with it.

### Running the bot server
First of all you should configure the project.
Copy the config file from it's dist:
```
cp bot/config.py.dist bot/config.py
```
Then fill up the copied config with some secrets.
To fetch the secrets address to [duker](https://about.me/duker33).

To run the server itself choose one of two options: python venv (recommended) or selenium.


#### Option 1: Running with python venv (recommended)
Since http driver doesn't work with docker, we should run it on the local machine.
It's not good level of dev env isolation, but it's working temporary decision.

```bash
python3 -m venv venv/
source venv/bin/activate
python3 main.py  # run server
pytest test/  # run tests
```

#### Option 2: Running with docker
**Note:** Only selenium driver works with docker.
It's because of IQParks webpanel uses old TLS1.0 encrypting.
To use http driver run server with python venv/
See #2 issue for details.

Now the bot server is ready to start:
```
docker-compose up -d app
```

You can see the server logs with the standard docker tools:
```
docker-compose logs app
```
