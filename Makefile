SENV=. ./env.sh
HIDE=@

flake8:
	$(HIDE)flake8 --config config/flake8 .

eslint:
	$(HIDE)grunt lint

test:
	$(HIDE)$(SENV)python manage.py test forum
