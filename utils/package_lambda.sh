#!/bin/bash
## Script to package and publish the lambda function
## Assumes environment has awscli installed and configured with appropriate credentials

# Where am I?
_script=${BASH_SOURCE[0]}
_base="$(dirname ${_script})"

_staging_dir=staging
_artifact=build.zip

_lambda_name=BreastEasier_MVP

pushd ${_base}/..

# clear Staging directory if it exists
if [ -d ${_staging_dir} ]; then
    echo Clearing ${_staging_dir} directory
    rm -rf ${_staging_dir}
fi

if [ -e ${_artifact} ]; then
    echo Deleting stale ${_artifact}
    rm -f ${_artifact}
fi

# create staging directory
echo Creating ${_staging_dir} directory
mkdir ${_staging_dir}

# install requirements to staging
echo Installing 3rd Party requirements to ${_staging_dir}
pip install -r ./requirements.txt -t ./${_staging_dir}/

# copy src to staging
echo copying src to ${_staging_dir} dir
cp -R ./src/ ./${_staging_dir}/

# zip staging dir
echo Packaging ${_staging_dir} directory into ${_artifact}
pushd ${_staging_dir}
zip -r ../${_artifact} .
popd

# post to aws
echo Posting ${_artifact} to Lambda:${_lambda_name}
aws lambda update-function-code --function-name ${_lambda_name} --region us-east-1 --zip-file fileb://${_artifact}

popd