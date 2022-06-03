function does_lambda_exist() {
  aws lambda get-function --function-name $1 > /dev/null 2>&1
  if [ 0 -eq $? ]; then
    return True
  else
    return False
  fi
}

#does_lambda_exist $1
does_lambda_exist TestLoader9
#aws lambda get-function --function-name TestLoader9 > /dev/null 2>&1
#$?

#if [ 0 -eq $? ]; then return True fi