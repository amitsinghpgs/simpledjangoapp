this is a simple django app to share quotes.
it can be dockerized

docker build -t my-django-app .

docker run --name some-django-app -p 8000:8000 -d my-django-app

Then go to localhost:8080 view the website