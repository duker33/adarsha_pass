[![Hits-of-Code](https://hitsofcode.com/github/duker33/adarsha_pass)](https://hitsofcode.com/view/github/duker33/adarsha_pass)

# Bot to order passes to Adarsha org

Bot orders passes throw [iq-park](http://iqpark-msk.ru/) business centre to [Adarsha organization](https://vk.com/adarsha_yoga) based in Moscow, Russia.

It's not open source project, since it's not possible to reuse it. But it's open code one.


## Running the bot server
First of all you should configure the project.
Copy the config file from it's dist:
```
cp bot/config.py.dist bot/config.py
```
Then fill up the copied config with custom values.

Now the bot server is ready to start:
```
docker-compose up -d app
```

You can see the server logs with the standard docker tools:
```
docker-compose logs app
```
