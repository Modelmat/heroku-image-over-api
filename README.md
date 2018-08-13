# Image over API
A web app to return images from an api.
Currently runs on Heroku.

The following GET request parameters are supported:

| Name    | Required | Description                                                                                                                                                                                           |
|---------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| url     | True     | A url which returns a JSON response                                                                                                                                                                   |
| query   | True     | This uses [jsonpath](https://github.com/kennknowles/python-jsonpath-rw) to parse the query expression. An online evaluator exists [here](http://jsonpath.com/) so that you can test your expressions. |
| suffix  | False    | Appends a string to the value returned by the jsonpath expression.                                                                                                                                    |
| prefix  | False    | Prepends a string to the value returned by the jsonpath expression.                                                                                                                                   |
| replace | False    | Replaces the first string with the second (e.g. &replace=first,second) in the value returned by the jsonpath expression.                                                                              |

The expected return value from the query should be approximately a url, the suffix, prefix, and replace parameters can increase the chance of this.

If an error occurs when fetching the URL or the return value a standard text response with an error message will be supplied; unknown errors will respond with a full python traceback. 
Please send this to the issues.
