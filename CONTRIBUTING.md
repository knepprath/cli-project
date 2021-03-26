# Contributing to klickbrick CLI

## Prerequisites
To work on this project your development environment should have the following prerequisites install:

- Python 3.7+ should be executable in your shell's path environment.
- The build automation tool `make`. On macOS, install command line tools by running the command `xcode-select 
  --install`
- Install Poetry using the instructions specified in the [documentation](https://python-poetry.org/docs/#installation).

## Development
This project uses Poetry for dependency management and packaging.

To install dependencies for development, run: 
```
poetry install 
```

To run locally:
```
poetry run klickbrick help
```

## Testing
Use Make to run tests

For unit tests:

```
make test
```

Integration test:
```
make integration
```

Behave Integration tests are implemented by invoking the CLI through the package installed in the Poetry virtual
 environment. 
 
Individual tests can be run by Feature:

`behave -i cli.feature`

Or individual scenarios:

`behave -n 'Document Available Commands'`


## Publishing
*NOTE:* This project is currently publishing to TestPyPI repository because the project is for educational purposes. 

Update the `version` in `pyproject.toml`.

To publish a build to PyPI the commit needs to be tagged

```
git tag -a v1.2
git push --tags
```

## Contributing

1. Create your feature branch (`git checkout -b feature/fooBar`)
1. Commit your changes (`git commit -am 'Add some fooBar'`)
   - NOTE: this project uses git pre-commit hooks to format and lint code changes to align with standard conventions. 
1. Push to the branch (`git push origin feature/fooBar`)
1. Create a new Pull Request


## Release History

* 0.0.x
    * Proof of Concept