from pytrends.request import TrendReq
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/trends/iot')
def iot():

    keywords = request.args.get('keywords').split(',')

    pytrends = TrendReq(hl='en-US', tz=360)

    pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')

    df = pytrends.interest_over_time()

    obj = { "data": []}

    for keyword in keywords:
        metrics = {"keyword": keyword}
        metrics["values"] = []
        for key in df[keyword].keys():
            metrics["values"].append({
                "timestamp": key.isoformat(),
                "interest": int(df[keyword][key])
            })
        obj["data"].append(metrics)

    return json.dumps(obj)

if __name__ == "__main__":
    app.run()

