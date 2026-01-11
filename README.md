# Django5Blog
Pierwszy projekt Django5

stworzenie superużytkownika: `python manage.py createsuperuser`

uruchomienie serwera lokalnie: `python manage.py runserver`

ORM - Object-Related Mapping - mapowanie relacyjno-obiektowe

# Polecenia zarządzające
1. Utworzenie struktury plików dla nowego projektu Django:
`django-admin startproject NAZWA_PROJEKTU`
2. Utworzenie struktury plików dla nowej aplikacji Django:
`python manage.py startapp NAZWA_APLIKACJI`
3. Zastosowanie wszystkich migracji baz danych:
`python manage.py migrate`
4. Utworzenie migracji dla modeli aplikacji:
`python manage.py makemigrations NAZWA_APLIKACJI`
5. Wyświetlenie instrukcji SQL, które zostaną wykonane podczas n migracji:
`python manage.py sqlmigrate NAZWA_APLIKACJI 000n`
6. Uruchomienie serwera programistycznego:
`python manage.py runserver`
7. Uruchomienie serwera programistycznego z podaniem hosta i portu oraz ze wskazaniem plik ustawień:
`python manage.py runserver 127.0.0.1:8001 --settings=NAZWA_PROJEKTU.settings`
8. Uruchomienie powłoki Django:
`python manage.py shell`
9. Utworzenie super użytkownika:
`python manage.py createsuperuser`

