#!/usr/bin/env bash

mkdir data;
cat sql/base.sql | sqlite3 data/service.db;
