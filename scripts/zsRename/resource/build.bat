@Echo off
pyuic5 -x dialog.ui -o ../python/app/ui/layout.py
echo CREATE: %file_name% -- %python%