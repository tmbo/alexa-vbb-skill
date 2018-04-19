# Alexa S-Bahn Skill

Stores a home station and when ever asked for it replies with the next
departure times.




## Development Setup

1. Make sure serverless is installed (to deploy functions to AMZN Lambda):
```bash
npm install serverless -g
```

2. Setup your AWS lambda account (creating keys / secrets for serverless to deploy)
https://serverless.com/framework/docs/providers/aws/guide/credentials/.

3. Reach out to vbb and ask them for an access token. Using their "development"
system is fine, have never experienced issues with it: [VBB REST API](http://www.vbb.de/de/article/fahrplan/webservices/schnittstellen-fuer-webentwickler/5070.html#rest-schnittstelle)

4. Add VBB token to `config.py`.

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

