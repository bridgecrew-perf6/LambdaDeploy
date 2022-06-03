#!/bin/bash
function create_or_update_lambda() {
    aws lambda list-functions >> res.json
    val1=$(grep $1 res.json)
    rm res.json
    declare -i length
    length=${#val1}
    #echo $length
    if [ $length -gt 0 ]; then
        
        aws lambda update-function-code --function-name  $1 --zip-file "fileb://TweetLoaderZIP.zip"
    else#
        
        aws lambda create-function --function-name $1 --runtime "python3.8" --role "arn:aws:iam::290544014146:role/LambdaRole" --zip-file "fileb://TweetLoaderZIP.zip" --handler lambda_function.lambda_handler
        
    fi
}

#does_lambda_exist $1
create_or_update_lambda $1

