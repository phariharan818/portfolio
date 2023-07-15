#!/bin/bash

tmux kill-session -a

cd ~/priya-portfolio

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s flask-session 'python app.py'

git reset origin/main --hard 

flask run
