# cplace-github-automation

Github Action scripts to automate Efecte ticket workflows.


## Requirements

- add new Users to existing repos
  - name
  - justification
  - access rights

- create new repo
  - owner
  - reason
  - name

## Features

Pull, filter and sort Github Managment related tickets from Efecte.
Depending on their status, use Github action to add/remove user from repos, create new repos etc.


## Implementation

### Credentials

Credentials (tokens, passwords, etc.) are stored using Github secrets. This ensures, that access to
production APIs are stored securely and encrypted.


### Trigger

The Github action is intended to run as a (nightly) cron job. This might be suboptimal for
quick response times to tickets.


### Integrations

The Scripts make use of the Github and Efecte rest api.