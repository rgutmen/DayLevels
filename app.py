from utils import getTodayDBFormat
from flask import Flask, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Test the API
@app.route('/ping')
def ping():
    return jsonify({"answer":"pong!"})

#http://127.0.0.1:5002/levels/cl/20220712/20220718
@app.route('/levels/<string:market>/<string:date_start>/<string:date_end>', methods=['GET'])
def getLevelsPerDate(market, date_start, date_end):
    """Send the information from the DB according the dates and markets specified

    Args:
        market (_type_): _description_
        date_start (_type_): _description_
        date_end (_type_): _description_

    Returns:
        _type_: _description_
    """    """"""
    connection_obj = sqlite3.connect('db.sqlite3')
    cursor_obj = connection_obj.cursor()
    rowList = cursor_obj.execute('''SELECT * FROM '''+ market +''' WHERE Date BETWEEN '''+ date_start +''' AND ''' + date_end + ''';''').fetchall()
    listita = []
    for elem in rowList:
        listita.append(dict(zip([c[0] for c in cursor_obj.description], elem)))
    connection_obj.close()
    return jsonify(listita)


#http://127.0.0.1:5002/levels/cl/
@app.route('/levels/<string:market>', methods=['GET'])
def getLevels(market):
    """Send the information from the last register added in the DB, at opening time, RTH

    Args:
        market (_type_): _description_

    Returns:
        _type_: _description_
    """
    todayDB = getTodayDBFormat()
    connection_obj = sqlite3.connect('db.sqlite3')
    cursor_obj = connection_obj.cursor()
    rowList = cursor_obj.execute('''SELECT * FROM '''+ market.get('tableName') +''' WHERE date = '''+ todayDB +''';''').fetchone()
    rowDict = dict(zip([c[0] for c in cursor_obj.description], rowList))
    connection_obj.close()
    return {"Date": rowDict.get('Date'), 
            "Market": market,
            "stdP3": rowDict.get('stdP3'),
            "stdP2": rowDict.get('stdP2'), 
            "stdP1": rowDict.get('stdP1'), 
            "Open": rowDict.get('Open'), 
            "stdN1": rowDict.get('stdN1'), 
            "stdN2": rowDict.get('stdN2'), 
            "stdN3": rowDict.get('stdN3')
            }


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
