sudo aptitude install vim git cscope python-setuptools python-pip libxml2-dev libxslt-dev python-dev lib32z1-dev
postgresql postgresql-contrib python-psycopg2 libpq-dev

# install keroku CLI
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
# install python packages
sudo pip install Django markdown requests lxml beautifulsoup4 south virtualenv gunicorn dj-database-url dj-static
django-toolbelt django-storages boto cssselect

# set git color output
git config --global color.ui true
