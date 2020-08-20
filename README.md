# cli-project
*NOTE:* This project is a CLI built for educational purposes. 

## Testing
To run unit tests `python -m unittest discover -b`

To execute integration tests run `behave`


## Publish
*NOTE:* This project is currently publishing to TestPyPI repository because the project is for educational purposes. 

To publish a build to PyPI the commit needs to be tagged

```
git tag -a v1.2
git push --tags
```

