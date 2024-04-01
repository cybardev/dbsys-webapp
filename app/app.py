import urllib.parse as urlparse

import MySQLdb
from flask import Flask, Response, redirect, render_template, request

from .db import Database
from .utils import sanitize_input


def app_factory(DB_HOST: str, DB_USER: str, DB_PASSWORD: str, DB_NAME: str) -> Flask:
    """Factory function to create a Flask web app

    Args:
        DB_HOST (str): hostname for database server
        DB_USER (str): username for database server
        DB_PASSWORD (str): password for database server
        DB_NAME (str): name of database to connect to

    Returns:
        Flask: web app object to run
    """
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        """Render landing page with input form for table name

        Returns:
            str: html template for index page
        """
        return render_template("index.html")

    @app.route("/error/<string:msg>")
    def error_page(msg: str) -> str:
        """Render error page with info

        Returns:
            str: html template for error page
        """
        return render_template("error.html", msg=msg)

    @app.route("/table", methods=["POST"])
    def show_table() -> str:
        """Show table from name specified in text input form

        Returns:
            str: html template for table view
        """
        name = request.form.get("tname")
        try:
            with Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) as db:
                db.cursor.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s",
                    (name,),
                )
                headers = (h[0] for h in db.cursor.fetchall())
                db.cursor.execute(f"SELECT * FROM {sanitize_input(name)}")
                data = db.cursor.fetchall()
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            return redirect(f"/error/{urlparse.quote_plus(str(e))}")
        return render_template("table.html", tname=name, theaders=headers, tdata=data)

    @app.route("/supplier", methods=["POST"])
    def add_supplier() -> Response:
        """Add a supplier given info in input form

        Returns:
            Response: response from endpoint to redirect to
        """
        try:
            with Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) as db:
                details = {k: sanitize_input(v) for k, v in request.form.items()}
                db.cursor.execute(
                    "INSERT INTO suppliers(supplier_id, name, email) VALUES (%s, %s, %s)",
                    (details["sid"], details["sname"], details["semail"]),
                )
                for num in details["stel"].split(","):
                    db.cursor.execute(
                        "INSERT INTO suppliers_telephone(supplier_id, number) VALUES (%s, %s)",
                        (details["sid"], num.strip()),
                    )
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            return redirect(f"/error/{urlparse.quote_plus(str(e))}")
        return redirect("/")

    @app.route("/expenses", methods=["POST"])
    def annual_expenses() -> str:
        """Show a table of annual expenses between two given years

        Returns:
            str: html template for expenses view
        """
        start_yr = int(request.form.get("startyear"))
        end_yr = int(request.form.get("endyear"))
        try:
            with Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) as db:
                db.cursor.execute(
                    """
                    SELECT YEAR(orders.order_date), SUM(order_parts.quantity * parts.price)
                    FROM order_parts, orders, parts
                    WHERE orders.order_id = order_parts.order_id
                    AND order_parts.part_id = parts._id
                    AND YEAR(orders.order_date) BETWEEN %s AND %s
                    GROUP BY YEAR(orders.order_date)
                    ORDER BY YEAR(orders.order_date) DESC;
                    """,
                    (start_yr, end_yr),
                )
                data = db.cursor.fetchall()
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            return redirect(f"/error/{urlparse.quote_plus(str(e))}")
        return render_template(
            "expenses.html",
            start_yr=start_yr,
            end_yr=end_yr,
            tdata=data,
        )

    @app.route("/budget", methods=["POST"])
    def budget_projection() -> str:
        """Show a table of annual expenses for a given number of years
           after latest entry adjusted for inflation

        Returns:
            str: html template for budget view
        """
        years = int(request.form.get("years"))
        rate = float(request.form.get("rate"))
        try:
            with Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) as db:
                db.cursor.execute(
                    """
                    SELECT YEAR(orders.order_date), SUM(order_parts.quantity * parts.price)
                    FROM order_parts, orders, parts
                    WHERE orders.order_id = order_parts.order_id
                    AND order_parts.part_id = parts._id
                    GROUP BY YEAR(orders.order_date)
                    ORDER BY YEAR(orders.order_date) DESC
                    LIMIT 1;
                    """
                )
                data = db.cursor.fetchone()
                last_yr = int(data[0])
                total_expenses = float(data[1])
                tdata = [
                    [last_yr + i, round(total_expenses * (1 + rate / 100) ** i, 2)]
                    for i in range(1, years + 1)
                ]
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            return redirect(f"/error/{urlparse.quote_plus(str(e))}")
        return render_template("budget.html", years=years, rate=rate, tdata=tdata)

    return app
