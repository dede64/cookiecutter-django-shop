# Step by step guide

## 1. Set default python executable to python3.x
* Check if python 3.x is installed.
    * If not, install python>=3.5.
* Check if command `python` opens python3.x
    * If command `python` opens a python3.y, you will need to set the default python executable by these commands:
    * `sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 2`
    * `sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 3`
    * now by default will be used the 3.x version
    * (it can be reverted back to python2.y by running command: `sudo update-alternatives --config python` and selecting 2.y version)

## 2. Install required dependencies

* Run these commands:
    * `sudo apt install nodejs npm python3-pip`
    * `pip3 install --user pipenv cookiecutter autopep8`
    * `PATH="$(python -m site --user-base)/bin:${PATH}"`

## 3. Run the cookiecutter to kickstart the project

* Run this command:
    * `cookiecutter https://github.com/dede64/cookiecutter-django-shop`
* You will be asked few questions about how you want to setup your project
    * ### project_name
        * Your project's human-readable name, capitals and spaces allowed.
    * ### project_slug
        * Your project's slug without dashes or spaces. Used to name your repo and in other places where a Python-importable version of your project name is needed.
    * ### app_name
        * Name of django app inside the project
    * ### appName
        * app_name in camelCase
    * ### description
        * Describes your project and gets used in places like README.rst and such.
    * ### author_name
        * This is you! The value goes into places like LICENSE and such.
    * ### email
        * The email address you want to identify yourself in the project.
    * ### virtual_host
        * The domain name you plan to use for your project once it goes live. Note that it can be safely changed later on whenever you need to.
    * ### version
        * The version of the project at its inception.
    * ### timezone
        * The value to be used for the TIME_ZONE setting of the project.
    * ### python_version
        * Type here the version of python you have installed on your system.
    * ### dockerize
        * Indicates whether the project should be configured to use Docker and Docker Compose. The choices are:
            * 1) Do not use docker
            * 2) Use docker serving http
            * 3) Use uwsgi
            * 4) Use django behind an NGiNX proxy (recommanded)
    * ### use_i18n
        * Indicates whether the project should be configured to use Django Parler, supporting more than one language.
    * ### languages
        * Language codes of languages which will be supported by the app separated by comma (`en, de`)
    * ### use_paypall
        * Whether the shop will support paypal payments
    * ### use_stripe
        * Whether the shop will support stripe payment gate for payments with a card
    * ### use_sendcloud
        * Whether the shop will support sendcloud.
        * (SendCloud is a shipping integration that automatically collects shipping information when a customer buys a product in the shop.)
    * ### printable_invoice
        * Whether the shop will support printable invoice
    * ### delivery_handling
        * https://django-shop.readthedocs.io/en/latest/reference/delivery.html
        * #### partial
            * Items inside an order can be sent partialy (In separated packages)
        * #### common
            * Order will be shipped as a one inseperable unit.
        * #### n
    * ### product_model
        * https://django-shop.readthedocs.io/en/latest/reference/product-models.html
        * #### polymorphic
            * If you have different kinds of products, each requiring their own concrete product model.
        * #### smartcard
            * If you have one concrete product model for all products in your shop.
        * #### commodity
            * If you want to use a freeform CMS page to describe your products. It is usually the best solution if you only have a handful of products, or if the kind of product differs a lot.
    * ### use_compressor
        * Django compressor compresses linked and inline JavaScript or CSS into a single cached file.
        * ! When set to false app will not work (from my testing)
    * ### use_elasticsearch
        * Django elasticsearch DSL is a package that allows indexing of django models in elasticsearch. It is built as a thin wrapper around elasticsearch-dsl-py so you can use all the features developed by the elasticsearch-dsl-py team.
    * ### stock_management
        * https://django-shop.readthedocs.io/en/latest/reference/inventory.html
        * #### simple
            * A simple approach to keep track on the product’s quantity in stock, is to store this information side by side with the product model.
        * #### inventory
            * Sometimes it is not enough to just know the current number of items of a certain product. Consider the use case, where a product is short in supply but the next incoming delivery is already scheduled.
        * #### n
            * Shop will not manage remaining stock of items.
    * ### debug
        * Debug settings for django
        * ! Must be set to False when dockerize is enabled (not 0)
