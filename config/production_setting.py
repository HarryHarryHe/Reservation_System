# -*- coding: utf-8 -*-
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:yourpassword@127.0.0.1/food_db?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

APP = {
    'domain':'mini.harrymall.cn'
}

RELEASE_VERSION="20191216001"