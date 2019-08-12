#!/bin/sh
export FLASK_ENV="development"
export DATABASE_URL="postgres://u4plazadev:pw4plazadev@localhost:5432/plazadev"
python run.py
