# alexa-skills

Alexa skills written using flask-ask and deployed with zappa to AWS Lambda.

## The code

Written using [flask-ask](https://github.com/johnwheeler/flask-ask).

## Deploying with zappa

zappa provides a way to deploy python wsgi application to AWS Lambda. This includes packaging dependencies and your application into a zip. 

AWS Lambda requires linux binaries. While zappa tries to override other platform binaries with the correct one on deploy, it's not perfect. I wound up spinning an EC2 with the Amazon AMI just for deploys.

Also zappa depends on virtualenv to gather dependencies and does not support conda at the moment. The is an [open PR to support it](https://github.com/Miserlou/Zappa/pull/108).

Configure AWS:

```
aws configure
```

You need to create a virtualenv and install the requirements:

```
cd skill-dir
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Deploy with zappa:

```
zappa init
zappa deploy dev
```

Save url and use when creating the Alexa skill at developer.amazon.com. In the configuration step, select HTTPS Endpoint and paste the url.  At SSL Certificate, select "My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority". NOTE that you must use amazon account used on the echo for creating the skill in order to test.

## Debugging skill

If you encounter a problem running your skill, in the AWS console, go to the lambda function -> monitoring -> view logs in cloudwatch.
