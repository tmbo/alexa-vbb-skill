# Alexa S-Bahn Skill

Stores a home station and when ever asked for it replies with the next
departure times.

## Get a VBB token
Reach out to vbb and ask them for an access token. Using their "development"
system is fine, have never experienced issues with it:

Enter the token into `config.py`

## Development Setup

Make sure serverless is installed (to deploy functions to AMZN Lambda):
```bash
npm install serverless -g
```

Setup your AWS lambda account (creating keys / secrets for serverless to deploy)
https://serverless.com/framework/docs/providers/aws/guide/credentials/.


## Setting up the project
```
mkvirtualenv alexa-sbahn
pip install -r requirements.txt
npm install
```

## Deploying the app
```
serverless deploy
```

