from flask import Flask, request, jsonify
from flask_cors import CORS
import get_record as gr

app = Flask(__name__)
CORS(app)

# http://localhost:5000/record?mac=&floorid=&date=&hour=
@app.route("/record", methods=['GET'])
def record():
        mac = request.args.get('mac')
        floor_id = request.args.get('floorid')
        date = request.args.get('date')
        hour = request.args.get('hour')
        function = int(str(int(mac is not None)) +  str(int(floor_id is not None)) +  str(int(date is not None)) + str(int(hour is not None)), 2)

        if function == 1:
                return jsonify(gr.get_record_with_hour(hour)),
        elif function == 2:
                return jsonify(gr.get_record_with_date(date)),
        elif function == 3:
                return jsonify(gr.get_record_with_date_and_hour(date, hour)),
        elif function == 4:
                return jsonify(gr.get_record_with_floorid(floor_id)),
        elif function == 5:
                return jsonify(gr.get_record_with_floorid_and_hour(floor_id, hour)),
        elif function == 6:
                return jsonify(gr.get_record_with_floorid_and_date(floor_id, date)),
        elif function == 7:
                return jsonify(gr.get_record_with_floorid_date_and_hour(floor_id, date, hour)),
        elif function == 8:
                return jsonify(gr.get_record_with_mac(mac)),
        elif function == 9:
                return jsonify(gr.get_record_with_mac_and_hour(mac, hour)),
        elif function == 10:
                return jsonify(gr.get_record_with_mac_and_date(mac, date)),
        elif function == 11:
                return jsonify(gr.get_record_with_mac_date_and_hour(mac, date, hour)),
        elif function == 12:
                return jsonify(gr.get_record_with_mac_and_floorid(mac, floor_id)),
        elif function == 13:
                return jsonify(gr.get_record_with_mac_floorid_and_hour(mac, floor_id, hour)),
        elif function == 14:
                return jsonify(gr.get_record_with_mac_floorid_and_date(mac, floor_id, date)),
        elif function == 15:
                return jsonify(gr.get_record_with_mac_floorid_date_and_hour(mac, floor_id, date, hour))

@app.route("/realtime", methods=['GET'])
def real_time():
        return gr.get_record_real_time()

if __name__ == '__main__':
        app.run('0.0.0.0', 5000, debug = True)