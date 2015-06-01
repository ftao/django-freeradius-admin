# Django Freeradius Admin


## Basic Features

### API and WEB UI for

* add user
* change user password
* suspend user
* add/edit/delete group
* add/remove user to/from group

## Develop

``` bash
### install requirements ###
$> pip install -r requirements.txt

### create sqlite3 databases ###
$> PYTHONPATH=./ django-admin syncdb --settings=djra.dev_settings

### create radius database ###
$> sqlite3 djra/data/radius.db < djra/freeradius/schema.sql 

### start the server ###
$> PYTHONPATH=./ django-admin runserver --settings=djra.dev_settings
```

## Ansible Playbook Automation

See [vpn-deploy-playbook](https://github.com/ftao/vpn-deploy-playbook) for detail.
