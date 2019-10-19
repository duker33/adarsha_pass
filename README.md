[![Hits-of-Code](https://hitsofcode.com/github/duker33/adarsha_pass)](https://hitsofcode.com/view/github/duker33/adarsha_pass)
[![PDD status](http://www.0pdd.com/svg?name=duker33/adarsha_pass)](http://www.0pdd.com/p?name=duker33/adarsha_pass)

# Bot to order passes to Adarsha org

Bot orders passes throw [iq-park](http://iqpark-msk.ru/) business centre to [Adarsha organization](https://vk.com/adarsha_yoga) based in Moscow, Russia.

It's not open source project, since it's not possible to reuse it. But it's open code one.

## Running the bot server
First of all you should configure the project.
Copy the config file from it's dist:
```
cp bot/config.py.dist bot/config.py
```
Then fill up the copied config with some secrets.
To fetch the secrets address to [duker](https://about.me/duker33).

To run the server itself choose one of two options: python venv (recommended) or selenium.


### Running with python venv
Since http driver doesn't work with docker, we should run it on the local machine.
It's not good level of dev env isolation, but it's working temporary decision.

```bash
python3 -m venv venv/
source venv/bin/activate
python3 main.py  # run server
pytest test/  # run tests
```

### Running with docker
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
