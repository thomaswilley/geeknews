# geeknews

GN is a cloud-native app template (seed) masquerading as a simple social news site and an homage to HackerNews. GN includes:

- python3+django1.7 web app foundation
- basic templates for class based views and user interactions
- user registration process incl. TOS acceptance step
- user profiles & account maintenance
- integrated local & remote devops workflow
- ready to scale to real world needs out of the box (via CloudFoundry)

## Cloud Native / 12-factor

A few things are involved to make a traditional python/django based web application cloud-native & following some key [12-factor](http://12factor.net/) requirements, starting with the following:

- Use environment variables for settings rather than files

> Related to this - django settings.py relies on a dict/object to hold a
couple different segments of database information, i.e., ENGINE, NAME,
etc. CloudFoundry provides a single database connection string as a session variable. To
enable djagno to instantiate its own objects this way, we'll use the  [dj-database-url](https://github.com/kennethreitz/dj-database-url) package which will allow us to specific the database connection string (in a .env file for local development or at command line) and ensure our django app consumes it rather than the dict/object in settings.py.

- Figure out how you want to handle your static files

> I took a shortcut here and equipped gunicorn to serve them for simplicity [whitenoise](https://github.com/evansd/whitenoise).

- Get your workflow refined so you don't need to deploy to CF every
   time you want to see changes - but maintain environment parity (close as possible)

> The heart of this is [foreman](https://github.com/ddollar/foreman) (or
if you'd rather stick to all python,
[honcho](https://github.com/nickstenning/honcho)).

## Get Started

Run locally with foreman and deploy when you need to. Foreman locally approximates what happens in production CloudFoundry by enabling environment variables and providing Procfile-based services orchestration. Your 'Procfile' contains your production process list and 'Procfile.dev' is what you'll use for development (e.g., replacing a gunicorn run with manage.py runserver). To run foreman with a specific Procfile including the -f switch. Store all environment variables (e.g., DATABASE_URL, DEBUG, etc) in a file named .env in the same directory as your Procfiles and foreman will read it prior to spooling up processes.

Pre-requisites:

1. Install postgres, create database called "gn_db" owned by the user
"django" with password "django". You could of course use a different
provider/info but you'll need to revise the DATABASE_URL
[accordingly](https://github.com/kennethreitz/dj-database-url).
2. Setup your virtualenv

```bash
$ python3 -m virtualenv --no-site-packages --distribute venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

In your .env file:
```bash
DEBUG=True
DATABASE_URL=postgres://django:django@127.0.0.1:5432/gn_db
SECRET_KEY=^169g==30u^6#j(gpto%n%xa-pe)!-4-09j509n@tvbba)n&03
STATIC_ROOT=/gnsite/static
```

And start your local environment with:
```bash
$ foreman start -f Procfile.dev
```

## Deploying To Pivotal CloudFoundry

### Pre-requisites:

1. Get yourself a PivotalWS account at [run.pivotal.io](https://run.pivotal.io)
2. Get the [CloudFoundry CLI](https://github.com/cloudfoundry/cli)
   (i.e., ``` $  brew tap pivotal/tap && brew install cloudfoundry-cli ```)
3. Setup a space or use the default space within your CF account
4. Authenticate your cli (i.e., ``` $ cf login ```)
5. Review your application's
   [manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html)
looks correct (i.e., ``` cat manifest.yml ```)

### Deploy

1. Create your PostgresDB instance on the free tier of the marketplace's
   provider (i.e., ``` $ cf create-service elephantsql turtle gn_db ```)
2. Create the app droplet and initiate the database (i.e., ``` $ cf push
   gn --no-route -c "bash ./init_db.sh" ```)
3. Push the app propertly which creates routes & starts normally (i.e.,
   ``` $ cf push gn ```)

We should be all set up & running and available the the URL provided by
CloudFoundry (which you can see with a ``` $ cf app gn ```). You can
tail logs with ``` $ cf logs gn ``` for debugging or ``` $ cf logs gn
--recent ``` for a snapshot. And of course scale as needed ``` $ cf scale gn -i 3 ```.

## Author

**Thomas Willey**
- <https://github.com/thomaswilley>
- <https://twitter.com/thomaswilley>

## License

Open sourced under the [MIT license](LICENSE).

## Todo

- SSL
- Enable live emails (currently emails only display in term/logs)
- More with CF environment variables

## Reference & Further Reading

- https://github.com/cloudfoundry
- https://pivotal.io
- [HN-inspired scoring algorithm](http://amix.dk/blog/post/19574)
- http://blog.banck.net/2014/12/deploying-a-django-application-to-cloud-foundry/

