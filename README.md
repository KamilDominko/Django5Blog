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

## Przejście z SQLite3 na PostgreSQL

Eksportujemy dane z SQLite3 za pomocą komendy:

`python manage.py dumpdata --indent=2 --output=FILENAME.json`

jednak to jest za mało, trzeba dodać dodatkowe parametry:

`python -Xutf8 manage.py dumpdata --indent=2 --output=FILENAME.json --natural-foreign --natural-primary`

`python -Xutf8` - włącza tryb UTF-8 w Pythonie na windows, bez tej flagi dump może generować błędy kodowania

`manage.py dumpdata` - eksportuje dane z bazy danych do JSON

`--indent=2` - formatowanie JSON dla czytelności

`--output=FILENAME.json` - zapisuje wynik do pliku FILENAME.json

`--natural-foreign` - zamiast zapisywać klucze obce jako ID, Django zapisuje je w formie "naturalnej", np:
zamiast: `"author": 17` będzie: `"author": ["kamil"]`
dzięki temu PostgreSQL nie musi mieć takich samych ID jak SQLite; relacje many-to-many mogą się poprawnie odtworzyć, nie ma konfliktów z `contenttypes`

`--natural-primary` - tak samo dla kluczy głównych, np:
zamiast `"pk": 42` będzie `"pk": "my-slug"`
