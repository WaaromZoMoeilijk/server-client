
cd /var/www/pi/pidjango && python3 -m venv djenv && # if manual: from here you get (djenv) on the command line left from the prompt.
source djenv/bin/activate && # next time try withour 3
python -m pip install django gunicorn && 
# werkt alleen met sudo ervoor
django-admin startproject pidjango . && 
python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser && DJANGO_SUPERUSER_PASSWORD=roma2- DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=h.timmermans@kurkshop.nl ./manage.py createsuperuser --no-input && #sudo cp /home/pi/pidjango/djenv/lib/python3.7/site-packages/django/contrib/admin/static/admin/css/base.css /home/pi/pidjango/static/admin/css && sudo chmod 777 * -R && # next line is to prevent that the database is readonly
sudo chmod 777 /var/www/pi/pidjango && systemctl restart apache2
