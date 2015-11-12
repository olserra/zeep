start zeep:
docker-compose run --service-ports zeepweb

start:
./node_modules/.bin/webpack --config webpack.config.js --watch
