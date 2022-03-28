from flask import render_template
import config

connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    connex_app.run(debug=True)
