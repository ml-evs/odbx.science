docker compose run --rm --entrypoint "certbot certonly --webroot -w /var/www/certbot --email admin@odbx.science --agree-tos --no-eff-email -d www.odbx.science -d optimade-index.odbx.science -d optimade.odbx.science -d optimade-misc.odbx.science -d odbx.science -d datalab.odbx.science -d api.odbx.science -d api-dev.odbx.science -d datalab-dev.odbx.science -d dcgat.odbx.science" certbot
