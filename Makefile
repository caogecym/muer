HIDE=@

flake8:
	$(HIDE)flake8 --config config/flake8 .

eslint:
	$(HIDE)grunt lint

django-test:
	$(HIDE)python manage.py test forum

browser-test:
	$(HIDE)grunt karma

lint: flake8 eslint

test: django-test browser-test eslint flake8
