#!bin/bash
function does_lambda_exist() {
  aws lambda get-function --function-name $1 > /dev/null 2>&1
  if [ 0 -eq $? ]; then
    local LFCTexists=True
    echo True
  else
    local LFCTexists=False
    echo True

  fi
}

echo $1
does_lambda_exist $1