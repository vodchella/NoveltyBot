#!/bin/bash

ROOT_PATH=$(cd $(dirname $0) && pwd);
ln -s ${ROOT_PATH}/novelty_reload.py /usr/bin/novelty_reload
ln -s ${ROOT_PATH}/novelty_manage_report.py /usr/bin/novelty_manage_report