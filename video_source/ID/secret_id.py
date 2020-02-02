#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def secret_client_file():
    for file in os.listdir('.'):
        if file.endswith(".json"):
            selected_id = os.path.join("ID", file)
            print('client_secret_id : ', selected_id)
            return selected_id


if __name__ == '__main__':
    secret_client_file()
