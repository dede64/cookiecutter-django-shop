# Cookiecutter for django-SHOP

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter), **cookiecutter-django-shop** is a set of templates
for jumpstarting a [django-SHOP](https://github.com/awesto/django-shop) project quickly.

Use these Cookiecutter Templates to run one of the demo merchant implementations.

* To get a first impression on its features.
* Select the configuration example which is the most similar to your own requirements. Then replace the
  product models and templates with your own implementations.


## Quick How-To

Install [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/), [pipenv](https://pipenv.readthedocs.io/en/latest/)
and [npm](https://www.npmjs.com/get-npm) onto your operating system, for instance

on Ubuntu

Check that your default Python is version 3.5 or later. In Ubuntu-18.04, Python version 2.7 is the default, therefore
activate Python-3.6 using:

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
```

Before installing **django-SHOP**, a few additional packages must be added:

```bash
sudo apt install nodejs npm python3-pip
pip install --user pipenv cookiecutter autopep8
```

on MacOS

```bash
sudo brew install node
pip install --user pipenv cookiecutter autopep8
```

then change into your projects directory and invoke

```bash
cookiecutter https://github.com/awesto/cookiecutter-django-shop
```

You will be asked a few question. If unsure, just use the defaults. This creates a directory named
`my-shop`, or whatever project name has been choosen. This generated directory is named the
*merchant implementation*. For simplicity let's refer to it as `my-shop` in the following
documentation. This directory is where the merchant keeps its configurations, adds his own Django
models and overrides the templates.


## Run django-SHOP demo locally

Running the django-SHOP demo locally is probably the best choice, when you want to experiment with
alternative product models, templates, etc. and hence want to edit the code generated by the
Cookiecutter template.

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

This demo uses SQLite as its database. It neither supports caching, nor full text searches, nor an
asyncrounous worker.

Please be patient during the first page loads, because media files have to be downloaded and
thumbnailed andthe latter is a time-consuming task.


## Run django-SHOP demo in Docker

Running the django-SHOP demo inside a Docker container, allows you to test all features such as full
text search using Elasticsearch, Redis caching, running asynchronous tasks and it uses Postgres
instead of SQLite as the database. All these services run in a separate Docker containers, all
managed by `docker-compose`.

There are three different options to run the merchant implementation of **django-SHOP** inside a
Docker container:
* `runserver`: is intended for local development, for those who do not want to setup their own
  virtual Python environment.
* `uwsgi`: is intended for testing a productive or staging system, without having set up NGiNX
  (see below).
* `nginx`: is intended for productive environments, where the application server runs behind NGiNX.

After generating the project using **Cookiecutter**, all of them can be build using these commands:

```bash
cd my-shop
docker-compose up --build -d
```


### Run django-SHOP in Docker using `runserver`

When asked by Cookiecutter: *Select dockerize*, choose `2 - runserver` and `debug="y"`, to build the
merchant implementation using Django's built-in `runserver`. This will start a webserver, listening
on the IP-address of the docker-machine and on port 9009 (if unsure invoke `docker-machine ip`).
Here the working directory is mounted inside your local file system. After editing a file, the
webserver is restarted, so this setup is well suited during development.

Point a browser onto `http://<docker-machine-ip>:9009/` and start surfing. To access the Django
admin interface, log in as *admin* with password *secret*.


### Run django-SHOP in Docker using `uwsgi`

In environments, accesible from the Internet, we shall never run the application server using
Django's `runserver`. By chosing `3 - uwsgi` for *dockerize*, Django runs as a
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) application runner. This configuration can be
used to run an unencrypted demo shop, for instance in a staging environment.

Point a browser onto `http://<docker-machine-ip>:9009/` and start surfing. To access the Django
admin interface, log in as *admin* with password *secret*.


### Run django-SHOP behind an NGiNX proxy

In the previous configuration, the **uWSGI** application runner is configured to listen on port 9009
and serve HTTP requests directly. In a productive environment, we usually want to use NGiNX as a
reverse proxy in front of our Django application server. This allows us to dispatch our services on
multiple domains. In addition, NGiNX also supports https via [Let's Encrypt](https://letsencrypt.org/).

First we must create two separate Docker containers. This step must be done only once per host.
Behind this setup, we can connect as many application servers as our machine can handle. In a
separte folder, named for instance `NGiNX-Proxy`, create a file named `docker-compose.yml` adding
the following content:

```yaml
version: '2.0'  # or later

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

Start both containers, the proxy together with its companion:

```bash
docker-compose up -d
```

If both containers are running, switch back to your the directory and recreate the project answering
Cookiecutter on *Select dockerize* with `4 - nginx`. This creates a template which again can be
built into a composition of Docker containers with our usual build command (see above).

Here it is important to note that the webserver is listening on the IP address referenced by the
answer given on the Cookiecutter question *virtual_host*. Then point a browser onto
`http://<virtual_host>/` and start surfing.
After a few minutes, the SSL-certificate shall be ready, then you can even browse using https.


## Where to proceed from here?

Now that you have a simple working project, it usually is much easier to evolve into a real project
for the merchant's needs. Remember that there are 3 different ways to arrange your product models:
 * `commodity`: If you want to use a freeform CMS page to describe your products. It is usually the
   best solution if you only have a handful of products, or if the kind of product differs a lot.
 * `smartcard`: If you have one concrete product model for all products in your shop.
 * `polymorphic`: If you have different kinds of products, each requiring their own concrete product
   model.

By answering the Cookiecutter builder with YES to `use_i18n`, multilingual support is added to the
project. Currently only English and German are configured, but this can easily be changed by
adopting the LANGUAGE parameters in the project's `settings.py`.

By answering the Cookiecutter builder with YES to `use_paypal`, [PayPal](https://www.paypal.com/)
support is added to the project. You have to apply for PayPal credentials and add them to your
environment or into the project's `settings.py` or through the environment variables
`PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`.

By answering the Cookiecutter builder with YES to `use_stripe`, [Stripe](https://stripe.com/)
support is added to the project. Currently you may use the sandbox credentials provided with the
demo, but feel free to apply for your own ones and add them to the appropriate parameters in your
`settings.py` or through the environment variables `STRIPE_PUBKEY` and `STRIPE_APIKEY`.

By answering the Cookiecutter builder with YES to `use_sendcloud`, [SendCloud](https://www.sendcloud.com/)
support is added to the project. You have to apply for your own ones credentials, since SendCloud
does not offer any sandboxing.
