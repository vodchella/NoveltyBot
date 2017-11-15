#!/bin/bash

ROOT_PATH=$(cd $(dirname $0) && pwd);
ln -s ${ROOT_PATH}/novelty_reload.py /usr/bin/novelty_reload
