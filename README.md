
Duck Decoys, Goose Decoys & Decorative Wood Carvings
===

Dux' Dekes is a family owned and operated business which takes pleasure in serving the
decorative decoy and the wood carving industry.

This website is designed to allow Jeff to manage the decoys on his website, and
allow his customers to browse his stock and place orders with ease.

Installing
===

To install the website, you must first create a virtualenv with Python 3:

	mkdir duxdekes && cd duxdekes
    virtualenv -p python3 --always-copy ./

Once you've created the virtualenv, you need to switch to the new virtualenv
and activate it:

    source bin/activate

Clone the repository, and switch to that directory. You'll need to install both
the systems requirements and the python requirements:

    sudo ./system-requirements.sh
	pip install -r requirements.txt

NOTE: You need a sort of up-to-date pip version to use the `-r` option. Once in a
virtualenv, you can upgrade your version of pip locally:

    pip install --upgrade pip

After that, you need to create the `local_settings.py` file, and fill in the
right values:

    cp duxdekes/local_settings.py{.example,}

Don't forget to edit the new `local_settings.py` file to add in your actual
database details and settings!

If everything was installed successfully, and you're ready to test and deploy,
you can use the Django manage.py script to do so:

    python manage.py collectstatic
    python manage.py migrate
	python manage.py check

That should do it!
