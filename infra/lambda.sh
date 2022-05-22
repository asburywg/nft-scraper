#!/usr/bin/env bash

PANDAS=False
if [ $1 == "rarity" ]; then
  LAMBDA=nft-scraper-rarity
  SCHEDULE="cron(0 20 * * ? *)" # daily 4PM EST
  DIR=nft-scraper/rarity/
  HANDLER=rarity_tools.lambda_handler
elif [ $1 == "opensea-details" ]; then
  LAMBDA=nft-scraper-opensea-details
  SCHEDULE="cron(30 20 * * ? *)" # daily 4:30PM EST
  DIR=nft-scraper/opensea/details/
  HANDLER=details.lambda_handler
elif [ $1 == "twitter" ]; then
  LAMBDA=nft-scraper-twitter
  SCHEDULE="cron(0 21 * * ? *)" # daily 5PM EST
  DIR=nft-scraper/twitter/
  HANDLER=twitter.lambda_handler
elif [ $1 == "merge" ]; then
  LAMBDA=nft-scraper-merge
  SCHEDULE="cron(30 21 * * ? *)" # daily 5:30PM EST
  DIR=analysis/
  HANDLER=merge.lambda_handler
  PANDAS=true
else
  echo "Specify project for predefined variables"
  exit 1
fi

### lambda configs
ACCOUNT=410190022654
REGION=us-east-1
TIMEOUT=300
MEMORY=512
ROLE=arn:aws:iam::410190022654:role/nft-scraper-lambda-role
RETRY=1

### build - RELATIVE TO infra/
mkdir temp/
rsync -av ../$DIR temp --exclude .git/
rsync -av ../common temp --exclude .git/ --exclude __pycache__/
cd temp/
pip3 install -r requirements.txt -t ./
chmod -R 755 .
zip -r lambda.zip .

### deploy
aws lambda get-function --function-name $LAMBDA >/dev/null 2>&1
if [ 0 -eq $? ]; then
  echo "Updating lambda '$LAMBDA' code"
  aws lambda update-function-code --function-name $LAMBDA --zip-file fileb://lambda.zip 2>&1 >/dev/null
  sleep 2
  aws lambda update-function-configuration --function-name $LAMBDA --handler $HANDLER --timeout $TIMEOUT --memory-size $MEMORY 2>&1 >/dev/null
else
  echo "Creating lambda '$LAMBDA'"
  aws lambda create-function --function-name $LAMBDA --runtime python3.9 --zip-file fileb://lambda.zip --handler $HANDLER --timeout $TIMEOUT --memory-size $MEMORY --role $ROLE 2>&1 >/dev/null
fi

aws lambda put-function-event-invoke-config --function-name $LAMBDA --maximum-retry-attempts $RETRY 2>&1 >/dev/null

if [ "$PANDAS" = true ] ; then
  echo "adding pandas layer"
  aws lambda update-function-configuration --function-name $LAMBDA --layers "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pandas:2" 2>&1 >/dev/null
fi

### cron
RULE=$(aws events put-rule --name $LAMBDA --schedule-expression "$SCHEDULE" --query RuleArn --output text)
aws lambda add-permission --function-name $LAMBDA --statement-id eventbridge-event --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn $RULE 2>&1 >/dev/null
aws events put-targets --rule $LAMBDA --targets '[{"Id": "'$LAMBDA'", "Arn": "arn:aws:lambda:'$REGION':'$ACCOUNT':function:'$LAMBDA'"}]' 2>&1 >/dev/null

### cleanup
cd ../
rm -rf temp/
