CURRENT STATE of this SETUP (may 2021)
======================================

This setup is tried at a Raspberry Pi, but has never run fully.

It is adviced to do the install manually, step by step, following server.py .

After this install, this is needed:

1. check pidjango/settings.py : it might live in a different directory because we dont want to overwrite it with some release.
2. if error about bootstrap4: python -m pip install bootstrap4
3. start virtual environment: source djenv/bin/activate
4. python manage.py makemigrtions
5. python manage.py migrate
6. s = systemctl restart apache2