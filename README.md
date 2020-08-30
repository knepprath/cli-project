# cli-project
*NOTE:* This project is for educational purposes. It is a CLI built for the fictional toy company called KlickBrick  

The KlickBrick CLI is design to be an extensible swiss army knife used by Developers across the engineering
 department. The CLI commands are intended to reduce friction from any part of the Software Development
  lifecycle. 

## Installation 
The initial iteration of the CLI has been designed for developers on macOS, but some commands will work on Windows
 and Linux as well. 
 
 

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

