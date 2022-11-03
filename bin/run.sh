#!/bin/zsh

flask --app ptrack --debug run --host=0.0.0.0
#flask --app ptrack --debug run --host=0.0.0.0 --port=80
#[ec2-user@ip-172-31-91-98 ~]$ sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000


# flask --app ptrack init-db

# pip install -r requirements.txt

# pytest
# coverage run -m pytest
# coverage report
# coverage html
# pytest tests/test_item.py -k test_index -s


# pip3 install waitress
# waitress-serve --call 'ptrack:create_app'
# [ec2-user@ip-172-31-91-98 ptrack]$ waitress-serve --port 5000 --call 'ptrack:create_app

# sudo systemctl daemon-reload
# sudo systemctl enable ptrack.service
# sudo chmod 644 /lib/systemd/system/ptrack.service
# start a service
# sudo systemctl start application.service
# sudo systemctl start application

# stop a service
# sudo systemctl stop application.service

# restart a service
# sudo systemctl restart application.service

# reload a service
# sudo systemctl reload application.service

# enable a service
# sudo systemctl enable application.service

# disable a service
#sudo systemctl disable application.service

# get the status log of a service
#systemctl status application.service


# deactivate
# pwd => /Users/eugenepark/PycharmProjects/ptrack
#source venv/bin/activate


# python setup.py bdist_wheel

# {project name}-{version}-{python tag} -{abi tag}-{platform tag}
# ptrack-1.0.0-py3-none-any.whl

#python -c 'import secrets; print(secrets.token_hex())'