set funda user & passwd in utils.py (TODO: move to settings)

install docker & docker-compose

best to build images before:
docker-compose build

drink coffee ...

use management command to scrape your saved funda houses:
docker-compose run zeepweb python manage.py manual_scrape


start zeep:
docker-compose run --service-ports zeepweb

start:
./node_modules/.bin/webpack --config webpack.config.js --watch
