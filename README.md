# py-puppetfile

[![Build Status](https://travis-ci.org/othalla/py-control-repository.svg?branch=master)](https://travis-ci.org/othalla/py-control-repository)

## Description

This module aims to manage a Puppet control repository hosted on Github.
It allow to manage Puppetfile's module (add, update, update) in a specific Puppet environment.

## Usage


## Refactor model 

```
control_repository = ControlRepository('orga', 'repo', 'token')

puppet_environment = control_repository.get_environent('production')
```

```
puppetfile = puppet_environment.get_puppetfile()

puppetfile.add_forge_module(module)
```

