#Git Analytics

Use this to Analytics your git log to:

- Generate Keyword of your project commit 
- Generate Committer Info & Commit count

##Setup

Requirements:

- Redis

1.Install Requirements

    sudo pip install -r requirements.txt
    pip install https://github.com/mitsuhiko/flask/tarball/master


2.Init Database(Run run.py on REPO PATH)

    flask --app=db initdb
    python get_data.py REPO_PATH

3.Start Server

    python server.py    