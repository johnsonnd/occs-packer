#!/bin/bash
if [ $# -ne 2 ]; then
    /bin/echo "Usage: $0 <role> <region>" >&2
    exit 1
fi

ROLE="$1"
REGION="$2"

creds=$(/usr/bin/curl --silent http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE)
export AWS_DEFAULT_REGION="$REGION"
export AWS_ACCESS_KEY_ID=$(echo $creds | jp.py AccessKeyId | sed -e 's/"//g')
export AWS_SECRET_ACCESS_KEY=$(echo $creds | jp.py SecretAccessKey | sed -e 's/"//g')
export AWS_SESSION_TOKEN=$(echo $creds | jp.py Token | sed -e 's/"//g')

/bin/echo "export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION"
/bin/echo "export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"
/bin/echo "export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"
/bin/echo "export AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN"

