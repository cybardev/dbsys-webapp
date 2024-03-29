#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse

from flask import Flask, render_template, request, redirect, url_for, Response
import MySQLdb


def main(args: argparse.Namespace) -> None:
    app = app_factory(args.HOST, args.USER, args.PASSWORD, args.DATABASE)
    app.run(debug=True, host="0.0.0.0", port=args.PORT)


def app_factory(DB_HOST: str, DB_USER: str, DB_PASSWORD: str, DB_NAME: str) -> Flask:
    app = Flask(__name__)

    def get_db_connection():
        conn = MySQLdb.connect(
            host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME
        )
        return conn

    @app.route("/")
    def index() -> str:
        """Render landing page with input form for table name

        Returns:
            str: html template for index page
        """
        return render_template("index.html")

    @app.route("/table", methods=["POST"])
    def show_table() -> str:
        name = request.form.get("tname")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'%s'",
            [name],
        )
        headers = cur.fetchall()
        cur.execute("SELECT * FROM %s", [name])
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("table.html", tname=name, theaders=headers, tdata=data)

    @app.route("/supplier", methods=["POST"])
    def add_supplier() -> Response:
        conn = get_db_connection()
        cur = conn.cursor()
        details = request.form
        cur.execute(
            "INSERT INTO suppliers(supplier_id, name, email) VALUES (%s, %s, %s)",
            (details["sid"], details["sname"], details["semail"]),
        )
        cur.execute(
            "INSERT INTO suppliers_telephone(supplier_id, numbers) VALUES (%s, %s)",
            (details["sid"], details["stel"]),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    @app.route("/expenses", methods=["POST"])
    def annual_expenses():
        pass

    @app.route("/budget", methods=["POST"])
    def budget():
        pass

    return app


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Group project for CSCI-3461, made by Group 13",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-s",
        "--server",
        dest="HOST",
        type=str,
        default="localhost",
        help="server to host webapp on",
    )
    parser.add_argument(
        "-n",
        "--port",
        dest="PORT",
        type=int,
        default=42818,
        help="port to serve webapp on",
    )
    parser.add_argument(
        "-d",
        "--database",
        dest="DATABASE",
        type=str,
        help="database to use for webapp",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--user",
        dest="USER",
        type=str,
        help="database to use for webapp",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="PASSWORD",
        type=str,
        help="database to use for webapp",
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(_args())
