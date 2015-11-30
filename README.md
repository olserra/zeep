set funda user & passwd in utils.py (TODO: move to settings)

install docker & docker-compose

best to build images before:
```bash
docker-compose build
```

drink coffee ...

use management command to scrape your saved funda houses:
```bash
docker-compose run zeepweb python manage.py manual_scrape
```

start zeep:
```bash
docker-compose run --service-ports zeepweb
```

start:
```bash
./node_modules/.bin/webpack --config webpack.config.js --watch
```
