SECRET_KEY = "dump-secret-key"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "podle",
    "tests",
)


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

PODLE_NEWSLETTER_NAME = "dummy_newsletter"
PODLE_RSS_FEED_GROUP_NAME = "dummy-group"
