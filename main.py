from pytrends.request import TrendReq
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.errorhandler(404) 
def not_found(e):
    return jsonify(
        error=True,
        message="this route doesn't exist"
    ), 404

@app.route('/trends/iot')
def iot():

    keywords_raw = request.args.get('keywords')
    
    if keywords_raw == None or len(keywords_raw) == 0:
        return jsonify(
            error=True,
            message="no keywords defined"
        ), 404

    keywords = keywords_raw.split(',')

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

    return jsonify(obj)

if __name__ == "__main__":
    app.run()

