**scrape saved houses from your private funda account....no particular use here ... just experimenting with scraping, hendrix (https://github.com/hendrix/hendrix) , geodjango and react js**

..... working towards using hendrix task (as an alternative to celery) for running the import as a scheduled task (now its a mangement command)

set funda user & passwd in utils.py (TODO: :)

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

run:
```bash
npm install .
```

start:
```bash
./node_modules/.bin/webpack --config webpack.config.js --watch
```

start zeep:
```bash
docker-compose run --service-ports zeepweb
```
