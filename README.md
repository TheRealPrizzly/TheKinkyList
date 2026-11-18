# The Kinky List

A romantic, gamified bucket list for couples (or more). Build a shared list, let a game choose what's next, assign each wish to one or more people, and check it off when it's done.

**Games**

1. **Kinky List**: draws from The Kinky List. Pick it, then choose one of four modes (each mode's page links to the others):
   - **Randomize**: optionally choose intensities and categories, then tap *Randomize* to draw one matching wish at random. Tap it again to start over with a fresh one, or tap *Add one more* to draw another alongside it, up to 8.
   - **Pick your favorite**: shows 8 options. Choose up to 3.
   - **Just ask!**: search the list and choose up to 10.
   - **Try new things!**: offers only wishes that have never been drawn, favoring categories you've explored least. You can accept or skip (3 skips) and accept up to 5.
2. **Truth or Dare**: played live on one screen, from your Truth or Dare list. Choose who's playing and, optionally, the intensities, and the game picks who goes first. On each turn, that person chooses *Truth* (a question to answer out loud) or *Dare*. Tick *Also dare from The Kinky List* to mix in wishes too, skipping any the player said *Not for me* to. A dare can be marked *Done it*, or *Save for later*, which puts it on their To-do page. *Done it* records a wish from The Kinky List as lived; a dare from the Truth or Dare list is only copied to The Kinky List (in the *Truth or Dare* category) when someone saves it for later.
3. **Would you rather**: played live on one screen, from your Would you rather list. Pick the intensities if you like, then draw a question ("Would you rather be tied up or do the tying?"). Read it aloud and everyone answers. Tapping a choice highlights it, and *Next question* draws another, with no repeats until you've seen them all.

Every Kinky List mode ends the same way: choose who each wish is for, confirm, and it appears on everyone's *To-do* page. An assignee checks it off, with an optional memory note, or answers whoever requested it:

- **Interested**: it stays on the To-do list, and they know you're keen.
- **Maybe eventually**: it goes back on the list, and they know you'd like to someday.
- **Not for me**: it goes back on the list, and nobody can give it to you for 6 months.

On a shared wish, *Maybe eventually* and *Not for me* only take you off it. Answers show up on the To-do page of whoever requested the wish until they dismiss them.

**Each wish** has an action, any number of categories, and an intensity: Sweet, Spicy or Sizzling.

**Our lists**: each space keeps one list per kind of game, each on its own tab of the *Lists* page.

| List | Played in | Starts with |
| --- | --- | --- |
| The Kinky List | Kinky List (all four modes) | The Kinky Bucket List, 136 wishes (`items/starter.py`) |
| Truth or Dare | Truth or Dare | 105 truths and 105 dares (`games/truths.py`, `games/dares.py`) |
| Would you rather | Would you rather | 100 questions (`games/would_you_rather.py`) |

Every new space starts with all three filled. On each tab you can add entries one at a time, remove any of them, *Clear the list*, or *Generate a list*, which adds back whichever of ours aren't on it: all of them on an empty list, or just the ones you removed. You can also import your own list (below). On The Kinky List, *Archive* keeps a wish out of the games without losing its history; *Remove* deletes it along with its to-dos and memories.

**Importing a list**: open *Import your own list* on a tab and paste one entry per line. Intensity is always optional and is a name or a number from 1 to 3. Tabs work in place of `|`, so rows copied from a spreadsheet import as they are. Anything already on the list is skipped.

- **The Kinky List**: `Action | Categories | Intensity`, with several categories separated by commas.
- **Truth or Dare**: `Text | Intensity`, added as truths or dares depending on what you pick above the box. Start a line with a `Truth` or `Dare` column to mix both in one paste.
- **Would you rather**: `First choice | Second choice | Intensity`, or the question written out with a single "or".

```text
Candlelit bath | Romance, Relaxing | Sweet
Dare | Kiss my neck for a full minute | Spicy
Would you rather be tied up or do the tying? | 3
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
- `collectstatic` names each CSS, JS and image file after its contents (`app.3f2a9c1b7d4e.css`). That way phones and the apps fetch the new version right after an update, instead of keeping an old copy. So run it after every `git pull`: until you do, pages that use a new static file fail with *Missing staticfiles manifest entry*.
- SQLite is the default and is plenty for a few people. To use PythonAnywhere MySQL instead:
  - `pip install mysqlclient`
  - add `DB_ENGINE=mysql` plus `DB_NAME`, `DB_USER`, `DB_PASSWORD` and `DB_HOST` to `.env` (see `.env.example`)
- "Live" updates use polling every 20 seconds, because PythonAnywhere web apps don't support websockets.
- Back up your data by downloading `db.sqlite3` from the **Files** tab.

## Mobile apps (App Store and Google Play)

The iPhone and Android apps live in `mobile/` and are built with [Capacitor](https://capacitorjs.com). They are a native shell that loads the live site, so deploying the site updates both apps. You only need a new store build after changing something in `mobile/`.

What the site already provides for the stores:

- **Account deletion**: *Profile → Delete account* (both stores require it in apps with sign-up).
- **Privacy policy**: `/privacy/`. Set `CONTACT_EMAIL` in `.env` so it shows a contact address.
- **18+ confirmation** at sign-up.
- **Installable web app**: `/manifest.webmanifest`, `/sw.js` and an `/offline/` page. Pages are never cached on the device.

**Tools:** Node.js LTS for everything; Android Studio to build and run the Android app; a Mac with Xcode (or a cloud Mac or cloud build service) for the iPhone app.

- **Java 21 for Android builds.** Android Studio bundles a newer Java that this Gradle version can't run on. Install JDK 21, point `JAVA_HOME` at it, and in Android Studio set *Settings → Build, Execution, Deployment → Build Tools → Gradle → Gradle JDK* to `JAVA_HOME`.
- **Emulator on Windows** needs the *Windows Hypervisor Platform* feature turned on, and runs far better with host GPU rendering (`emulator -avd <name> -gpu host`) and 4 GB of RAM.

**Setup after cloning** (in `mobile/`). The `android/` and `ios/` projects are already in the repo:

```bash
npm install
npx cap sync
```

`npm run assets` regenerates every iOS and Android icon and splash size from `mobile/assets/`.

**Try it on the Android emulator** against your local site (run `python manage.py runserver` first, with `10.0.2.2` in `ALLOWED_HOSTS`):

```bash
SITE_URL=http://10.0.2.2:8000 npx cap run android      # PowerShell: $env:SITE_URL="http://10.0.2.2:8000"; npx cap run android
```

**Before a store build**, set `PRODUCTION_URL` in `mobile/capacitor.config.ts` to the hosted https address, then run `npx cap sync` *without* `SITE_URL` set (the sync writes the URL into the native projects) and open the native project with `npx cap open android` or `npx cap open ios` to build and sign.

### Push notifications

The apps notify people when someone requests something from them, answers their request, checks off a wish they share, or joins their space. Notifications are sent through Firebase Cloud Messaging (FCM), which also delivers to iPhones through Apple's push service.

They only say who did something ("Sam requested something from you 💌"). Wish titles appear only for people who turn on *Show wish titles in notifications* on their profile, because notifications show on lock screens.

Push stays off, and the app asks for nothing, until both halves below are set up.

1. **Create a Firebase project** at [console.firebase.google.com](https://console.firebase.google.com). Google Analytics isn't needed.
2. **Android:** add an Android app with package name `com.thekinkylist.app`, download `google-services.json` and put it in `mobile/android/app/`.
3. **iOS** (on a Mac):
   - Add an Apple app with bundle ID `com.thekinkylist.app`, download `GoogleService-Info.plist` and add it to the `App` target in Xcode.
   - In Apple Developer, create an APNs key, then upload it in Firebase under *Project settings → Cloud Messaging*.
   - In Xcode, under *Signing & Capabilities*, add **Push Notifications**. *Background Modes → Remote notifications* is already set in `Info.plist`.
   - Run `npx cap sync ios`. It needs to create a symlink, which Windows can't do without Developer Mode.
4. **Server:**
   - In Firebase, go to *Project settings → Service accounts → Generate new private key*.
   - Upload the key to the server, outside the repository, and set `FCM_SERVICE_ACCOUNT_FILE` in `.env` to its path. It's a secret, so never commit it.
   - Reload the web app.
5. **Rebuild both apps** (`npx cap sync`, then build).

After that, the dashboard in the app shows *Turn on notifications*. Once someone allows it, their phone's token is saved in the `push.Device` table, and logging out of that phone removes it.

On a free PythonAnywhere account, outgoing requests are limited to an allowlist. Check that `fcm.googleapis.com` and `oauth2.googleapis.com` are reachable from a console before relying on it.

**Icons:** `python scripts/make_icons.py` redraws `static/icons/` and `mobile/assets/` (needs `pip install pillow`, which the site doesn't use).

## Sign in with Google

Once it's set up, *Continue with Google* appears on the login and sign-up pages, and *Connect Google* on the profile page.

- **In browsers**, the button opens Google's sign-in page.
- **In the Android app**, it opens Android's own account picker, because Google blocks its sign-in page inside apps.
- **In the iPhone app**, the button is hidden. Offering Google there means also offering Sign in with Apple (App Store rule 4.8).

New Google users still choose a display name and confirm they're 18 or older. The site keeps only Google's account number for them, not their email address or photo.

1. **Turn it on in Firebase** (the same project as push): go to *Build → Authentication → Get started → Sign-in method → Google → Enable*, pick a support email and save. This creates an OAuth client named *Web client (auto created by Google Service)*.
2. **Register your site with that client:** in the Google Cloud console for the same project, go to *APIs & Services → Credentials* and open the Web client.
   - Add these *Authorized redirect URIs*: `https://<your site>/google/callback/` and, for local testing, `http://localhost:8000/google/callback/`. Locally, open the site at `localhost` rather than `127.0.0.1`.
   - Copy its *Client ID* and *Client secret*.
3. **Set up the consent screen:** under *Google Auth Platform → Branding*, set the app name, a support email and your privacy page (`https://<your site>/privacy/`). Under *Audience*, publish the app. Until you do, only listed test users can sign in. The site only asks for basic scopes (`openid profile`), so Google doesn't need to review it.
4. **Configure the server:** add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to `.env` and reload. Keep the secret out of git. The server must be able to reach `oauth2.googleapis.com` and `www.googleapis.com`.
5. **Set up the Android app:**
   - In Firebase, go to *Project settings → Your apps → Android* and add the SHA-1 fingerprint of every key that signs the app. Test builds use your debug key; get its fingerprint with `keytool -list -v -keystore %USERPROFILE%\.android\debug.keystore -alias androiddebugkey -storepass android`. Store builds use Google Play's app signing key; find its fingerprint in Play Console under *Setup → App signing*.
   - Download `google-services.json` again into `mobile/android/app/`. The new copy names the Web client the app requests tokens for.
   - Rebuild with `npx cap sync android`, then build.

## Project layout

| Path | What's there |
|---|---|
| `accounts/` | Sign-up (with 18+ confirmation), Sign in with Google (`google.py`), profiles (display name, avatar color, notification previews), account deletion, privacy page |
| `push/` | Push notifications: devices, who gets notified and with what wording (`notify.py`), the Firebase sender (`fcm.py`); `static/js/push.js` runs inside the apps |
| `kinkylist/pwa.py` | Web app manifest, service worker and offline page |
| `mobile/` | Capacitor project for the iPhone and Android apps |
| `scripts/make_icons.py` | Draws the app icons and splash screens |
| `spaces/` | Shared spaces, invite codes, membership checks, dashboard |
| `items/` | The list and its categories: add, edit, archive, bulk import |
| `games/` | `registry.py` (game settings), `logic.py` (selection rules), views for every game |
| `assignments/` | Game sessions, assignments, check-off |
| `art/` | Deterministic SVG art generator and template tags |
| `templates/`, `static/` | Pages, theme CSS, Alpine components; `static/js/confirm.js` asks every "Are you sure?" question in the app's own dialog (`hx-confirm` or `data-confirm`) |
