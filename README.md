# Cookiecutter for django-SHOP

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter), **cookiecutter-django-shop** is a set of templates
for jumpstarting a **django-SHOP** project quickly.

> Note: This documentation refers to the upcoming release 1.0.0 of django-SHOP. If you are looking for
  version 0.12.x, please check here: https://github.com/awesto/cookiecutter-django-shop/tree/releases/0.12

Use these Cookiecutter Templates to run one of the demo merchant implementations.

* Use them to get a first impression on its features.
* Select the configuration example which is the most similar to your own requirements. Then replace the
  product models and templates with your own implementations.


## Quick How-To

Install [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/), [pipenv](https://pipenv.readthedocs.io/en/latest/)
and [npm](https://www.npmjs.com/get-npm) onto your operating system, for instance

on Ubuntu

```bash
sudo apt-get install python-cookiecutter pipenv autopep8 nodejs npm
```

on MacOS

```bash
sudo brew install cookiecutter pipenv autopep8 node
```

> Note: If `pipenv` is not available through your package manager, try with `pip install pipenv`.

then change into your projects directory and invoke

```bash
cookiecutter https://github.com/awesto/cookiecutter-django-shop
```

You will be asked a few question. If unsure, just use the defaults. This creates a directory named `my-shop`,
or whatever you have choosen. This generated directory is named the *merchant implementation*. For simplicity
let's refer to it as `my-shop` in the following documentation. This directory is where the merchant keeps its
configurations, adds his own Django models and overrides the templates.


## Run django-SHOP demo locally

Running the django-SHOP demo locally is probably the best choice, when you want to experiment with
alternative product models and hence want to edit the code generated by the Cookiecutter template.

When asked by Cookiecutter: *Select dockerize*, choose `1 - n`.

```bash
cd my-shop
pipenv install --sequential
npm install
pipenv run ./manage.py initialize_shop_demo
export DJANGO_DEBUG=1
pipenv run ./manage.py runserver
```

After the above job has finished, point a browser onto http://localhost:8000/ and login with user
*admin* and password *secret*.

This demo uses SQLite as its database. It does neither support caching, nor full text searches.


## Run django-SHOP demo in Docker

When asked by Cookiecutter: *Select dockerize*, and you choose `2 - http`, the merchant implementation is build with
Docker support, listening for HTTP on port 9009.

Running the django-SHOP demo inside a Docker container, allows you to test all features such as full text search, proper
caching, running asynchronous tasks and it uses a Postgres database, running in a separate container.

First, check that your Docker machine is running. If unsure invoke `docker-machine ip`.

```bash
cd my-shop
docker-compose up --build -d
```

Point a browser onto http://<docker-machine-ip>:9009/ and start surfing. Determine the IP address using
``docker-machine ip``.

In case you want to access the Django admin interface, log in as *admin* with password *secret*.


### Run django-SHOP behind an NGiNX proxy

In the previous configuration, the [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) application runner is
configured to listen on port 9009 for HTTP requests. There we can connect the browser directly onto the Docker machine's
IP address. In a productive environment, we might want to use NGiNX as a reverse proxy in front of our Django
application server. This allows us to dispatch our services on multiple domains. In addition it also supports https.

First we must create two separate Docker containers. This has to be done only once per host. Using this setup, we can
connect as many containers as our machine can handle. In a separte folder, named for instance `NGiNX-Proxy`, create a
file named `docker-compose.yml` and add this content:

```yaml
version: '2.0'

services:
  nginx-proxy:
    restart: always
    image: jwilder/nginx-proxy:latest
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - nginxcerts:/etc/nginx/certs:ro
      - nginxvhostd:/etc/nginx/vhost.d
      - /usr/share/nginx/html
      - /var/run/docker.sock:/tmp/docker.sock:ro
    networks:
      - nginx-proxy

  letsencrypt-nginx-proxy-companion:
    restart: always
    image: jrcs/letsencrypt-nginx-proxy-companion
    # environment:  # remove this fake certificate in production
    # - ACME_CA_URI=https://acme-staging.api.letsencrypt.org/directory
    volumes:
      - nginxcerts:/etc/nginx/certs:rw
      - /var/run/docker.sock:/var/run/docker.sock:ro
    volumes_from:
      - nginx-proxy

networks:
  nginx-proxy:
    external: true

volumes:
  nginxcerts:
  nginxvhostd:
```

Now start the proxy together with its companion:

```bash
docker-compose up -d
```

If both containers are running, switch back to your working directory and recreate the project answering Cookiecutter
on *Select dockerize* with `3 - uwsgi`. This creates a template which again can be built into a composition of Docker
containers using:

```bash
cd my-shop
docker-compose up --build -d
```

Here it is important that your server is listening on the IP address referenced by the answer given on question
*virtual_host*. Then point a browser onto http://<virtual_host>/ and start surfing.


## Where to proceed from here?

Now that you have a simple working project, it usually is much easier to evolve into a real project for the merchant's
needs. Remember that there are 3 different ways to arrange your product models:
 * `commodity`: If you want to use a freeform CMS page to describe your products. It is usually the best solution
   if you only have a handful of products, or if the kind of product differs a lot.
 * `smartcard`: If you have one concrete product model for all products in your shop.
 * `polymorphic`: If you have different kinds of products, each requiring their own concrete product model.

By answering the Cookiecutter builder with YES to `use_i18n`, multilingual support is added to the project. Currently
only English and German are configured, but this can easily be changed by adopting the LANGUAGE parameters in the
project's `settings.py`.

By answering the Cookiecutter builder with YES to `use_paypal`, [PayPal](https://www.paypal.com/) support is added to
the project. You have to apply for PayPal credentials and add them to your environment or into the project's
`settings.py` or through the environment variables `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`.

By answering the Cookiecutter builder with YES to `use_stripe`, [Stripe](https://stripe.com/) support is added to the
project. Currently you may use the sandbox credentials provided with the demo, but feel free to apply for your own
ones and add them to the appropriate parameters in your `settings.py` or through the environment variables
`STRIPE_PUBKEY` and `STRIPE_APIKEY`.

By answering the Cookiecutter builder with YES to `use_sendcloud`, [SendCloud](https://www.sendcloud.com/) support is
added to the project. You have to apply for your own ones credentials, as SendCloud does not offer any sandboxing.