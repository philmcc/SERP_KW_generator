# SERP_KW_generator

This code, will generate many keywords by srapping the google search results for a seed keyword and estractig related keywords and 'people also ask' suggestions.

The premise being that many of these resiults will prove to be low competition keywords that can be used to generate content.

Dynamodb is used for the storage engine and is automaticaly provisioned assuming account credentials are added through the AWS CLI.

The code also relies on a ValueSerp account in order to access their API