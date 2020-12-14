#!/usr/bin/env python3
import connexion
from connexion import NoContent

# memory-only metric storage
METRICS = []


def post_metrics():
    global METRICS
    METRICS = METRICS + connexion.request.json["metrics"]
    print(METRICS)
    return NoContent, (200)


app = connexion.App(__name__)
app.add_api("../openapi/telemetry.yml")
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == "__main__":
    # run our standalone gevent server
    app.run(port=8080, server="gevent")
