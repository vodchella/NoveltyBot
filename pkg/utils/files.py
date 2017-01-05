#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read_file_lines(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.read()
    f.close()
    return lines
