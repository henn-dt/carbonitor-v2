# app/cli/__init__.py
from flask import Flask
from app.cli.db import db_cli
from app.cli.seed import seed_cli

def init_cli(app: Flask):
    """Initialize all CLI commands."""
    #user_service.create_user()
    app.cli.add_command(db_cli)
    app.cli.add_command(seed_cli)