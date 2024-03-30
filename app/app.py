import MySQLdb
from flask import Flask, Response, redirect, render_template, request


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

    def get_db_connection() -> MySQLdb.connections.Connection:
        """Establish a connection with a MySQL server

        Returns:
            MySQLdb.connections.Connection: database connection object
        """
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
        """Show table from name specified in text input form

        Returns:
            str: html template for table view
        """
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
        """Add a supplier given info in input form

        Returns:
            Response: response from endpoint to redirect to
        """
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
    def annual_expenses() -> str:
        """Show a table of annual expenses between two given years

        Returns:
            str: html template for expenses view
        """
        start_yr = request.form.get("startyear")
        end_yr = request.form.get("endyear")
        conn = get_db_connection()
        cur = conn.cursor()
        query = (
            "SELECT YEAR(orders.order_date), SUM(order_parts.qty * parts.price) "
            + "FROM orders JOIN order_parts ON orders.order_id = order_parts.order_id "
            + "JOIN parts ON order_parts.part_id = parts._id "
            + "WHERE YEAR(orders.order_date) BETWEEN start_year AND end_year "
            + "GROUP BY YEAR(orders.order_date)"
        )
        cur.execute("%s", [query])
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template(
            "expenses.html",
            start_yr=start_yr,
            end_yr=end_yr,
            tdata=data,
        )

    @app.route("/budget", methods=["POST"])
    def budget() -> str:
        """Show a table of annual expenses for a given number of years
           after latest entry adjusted for inflation

        Returns:
            str: html template for budget view
        """
        years = request.form.get("years")
        rate = request.form.get("rate")
        conn = get_db_connection()
        cur = conn.cursor()
        query = (
            "SELECT YEAR(orders.order_date) AS order_year, "
            + "SUM(order_parts.qty * parts.price) * (1 + (rate / 100)) "
            + "FROM orders JOIN order_parts ON orders.order_id = order_parts.order_id "
            + "JOIN parts ON order_parts.part_id = parts._id "
            + "WHERE order_year >= (SELECT MAX(YEAR(order_date)) - N + 1 FROM orders) "
            + "GROUP BY order_year ORDER BY order_year DESC"
        )
        cur.execute("%s", [query])
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("budget.html", years=years, rate=rate, tdata=data)

    return app
