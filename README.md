# AI Lifestyle Manager

A Streamlit-based personal lifestyle tracker for habits, tasks, goals, and mood logging.

## Run locally

1. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Open the URL shown in your terminal.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in at https://share.streamlit.io.
3. Create a new app and connect your GitHub repo.
4. Set the main file path to `app.py`.

## Deploy on Heroku (optional)

1. Install the Heroku CLI.
2. Login and create an app:

```bash
heroku login
heroku create
```

3. Push your code:

```bash
git push heroku main
```

4. Open the app:

```bash
heroku open
```

> Note: this app saves data to a local JSON file, so persisted data may reset when the deployment instance restarts.
