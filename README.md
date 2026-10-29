# The Kinky List

A romantic, gamified bucket list for couples (or more). Build a shared list, let a game choose what's next, assign each wish to one or more people, and check it off when it's done.

**Games**

1. **Randomize**: optionally choose intensities and categories, then tap *Randomize* to draw one matching wish at random. Tap it again to keep drawing.
2. **Pick your favorite**: shows 8 options. Choose up to 3.
3. **Just ask!**: search the list and choose up to 10.
4. **Try new things!**: offers only wishes that have never been drawn, favoring categories you've explored least. You can accept or skip (3 skips) and accept up to 5.

Every game ends the same way: choose who each wish is for, confirm, and it appears on everyone's *To-do* page. An assignee checks it off, with an optional memory note.

**Each wish** has an action, any number of categories, and an intensity: Sweet, Spicy or Sizzling.

**Importing a list**: on *Our list*, open *Paste a whole list* and paste one wish per line as `Action | Categories | Intensity`. Categories and intensity are optional. Separate several categories with commas, and give the intensity as a name or a number from 1 to 3. Tabs work in place of `|`, so rows copied from a spreadsheet import as they are.

```text
Candlelit bath | Romance, Relaxing | Sweet
Skinny dip | Adventure | 3
Stargazing picnic
```

Built with Django 5.2, SQLite, htmx and Alpine.js (vendored in `static/vendor/`). There is no Node build step. The art is generated as SVG on the server, seeded per game and per item.

## Run locally

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
cp .env.example .env            # then set DEBUG=True and ALLOWED_HOSTS=localhost,127.0.0.1
python manage.py migrate
python manage.py runserver
```

Run the tests with `python manage.py test`.

## Deploy to PythonAnywhere

1. **Get the code.** Push this repo to GitHub, then open a **Bash console** on PythonAnywhere:
   ```bash
   git clone https://github.com/<you>/TheKinkyList.git
   cd TheKinkyList
   mkvirtualenv --python=python3.12 kinkylist
   pip install -r requirements.txt
   ```
2. **Configure.** Create `.env` in the project folder:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
   nano .env
   ```
   ```ini
   SECRET_KEY=<paste the generated key>
   DEBUG=False
   ALLOWED_HOSTS=<username>.pythonanywhere.com
   ```
3. **Set up the database and static files:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser   # optional, for /admin/
   ```
4. **Set up the web app.** On the **Web** tab:
   - Add a new web app, choose **Manual configuration**, then **Python 3.12**.
   - **Virtualenv**: `/home/<username>/.virtualenvs/kinkylist`
   - **Static files**: URL `/static/`, directory `/home/<username>/TheKinkyList/staticfiles`
   - **Security**: turn on *Force HTTPS*.
   - **WSGI configuration file**: replace its contents with:
     ```python
     import os
     import sys

     path = "/home/<username>/TheKinkyList"
     if path not in sys.path:
         sys.path.insert(0, path)

     os.environ["DJANGO_SETTINGS_MODULE"] = "kinkylist.settings"

     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
   - Click **Reload**, then visit `https://<username>.pythonanywhere.com`.

**Updating later:**

```bash
cd ~/TheKinkyList && git pull
workon kinkylist
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload** on the Web tab.

**Notes**

- On a free account, click **"Run until 3 months from today"** on the Web tab every few months to keep the site live.
- SQLite is the default and is plenty for a few people. To use PythonAnywhere MySQL instead:
  - `pip install mysqlclient`
  - add `DB_ENGINE=mysql` plus `DB_NAME`, `DB_USER`, `DB_PASSWORD` and `DB_HOST` to `.env` (see `.env.example`)
- "Live" updates use polling every 20 seconds, because PythonAnywhere web apps don't support websockets.
- Back up your data by downloading `db.sqlite3` from the **Files** tab.

## Project layout

| Path | What's there |
|---|---|
| `accounts/` | Sign-up (with 18+ confirmation) and profiles (display name, avatar color) |
| `spaces/` | Shared spaces, invite codes, membership checks, dashboard |
| `items/` | The list and its categories: add, edit, archive, bulk import |
| `games/` | `registry.py` (game settings), `logic.py` (selection rules), views for every game |
| `assignments/` | Game sessions, assignments, check-off |
| `art/` | Deterministic SVG art generator and template tags |
| `templates/`, `static/` | Pages, theme CSS, Alpine components |
