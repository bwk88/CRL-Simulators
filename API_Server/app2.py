from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔹 In-memory storage (acts like database)
sections_db = {
    "1": ["6", "4"],
    "2": ["3"]
}

# =========================================================
# DELETE API: /api/v1_0/ext/DeleteADCRSSectionData
# =========================================================
@app.route('/api/v1_0/ext/DeleteADCRSSectionData', methods=['DELETE'])
def delete_adcrs_section():

    try:
        data = request.get_json()

        # 🔹 Validate request body
        if not data:
            return jsonify({"reason": "incorrect value"}), 400

        node_id = data.get("node_id")
        section_id = data.get("section_id")

        if not node_id or not section_id:
            return jsonify({"reason": "incorrect value"}), 400

        # 🔹 Check if node exists
        if node_id not in sections_db:
            return jsonify({"reason": "resource method is not available"}), 404

        # 🔹 Check if section exists
        if section_id not in sections_db[node_id]:
            return jsonify({"reason": "resource method is not available"}), 404

        # 🔥 DELETE OPERATION
        sections_db[node_id].remove(section_id)

        return jsonify({
            "success_failure_flag": 0,
            "remarks": "Section deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({"reason": "internal_server_error"}), 500



# -----------------------------------------
# API: SaveADCRSADFAAreaData
# -----------------------------------------
@app.route('/api/v1_0/ext/SaveADCRSADFAAreaData', methods=['POST'])
def save_area_data():
    try:
        data = request.get_json()

        # ❌ No JSON / Empty body
        if not data:
            return jsonify({
                "reason": "incorrect value"
            }), 400

        action_flag = data.get("action_flag")
        area_name = data.get("area_name")

        # ❌ Validation checks
        if action_flag is None or area_name is None:
            return jsonify({
                "reason": "incorrect value"
            }), 400

        # Optional: stricter validation
        # if not isinstance(action_flag, int) or not isinstance(area_name, str):
        #     return jsonify({
        #         "reason": "incorrect value"
        #     }), 400

        # 🧪 Simulate processing
        print("Received:", data)

        # ✅ SUCCESS RESPONSE
        return jsonify({
            "success_failure_flag": 0,
            "remarks": "Success"
        }), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "reason": "internal_server_error"
        }), 500

# ---------------------------------------
# API: GetADCRSFreeTextMsgData (POST)
# ---------------------------------------
@app.route('/api/v1_0/ext/GetADCRSFreeTextMsgData', methods=['POST'])
def get_free_text_msg_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"reason": "incorrect value"}), 400

        from_day = data.get("From Day")
        from_month = data.get("From Month")

        # Validation
        if not from_day or not from_month:
            return jsonify({"reason": "incorrect value"}), 400

        # Optional: Validate numeric day
        try:
            from_day = int(from_day)
        except:
            return jsonify({"reason": "incorrect value"}), 400

        # -----------------------------
        # Generate Response Data
        # -----------------------------
        now = datetime.now()

        response_data = {
            "Generated Day": now.day,
            "Generated Month": now.strftime("%b"),   # Jan, Feb, etc.
            "Generated Year": now.year,
            "Generated Hour": now.hour,
            "Generated Minute": now.minute,
            "Generated Second": now.second
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"reason": "internal_server_error"}), 500

@app.route('/api/v1_0/ext/GetADCRSADFAAreaData', methods=['POST'])
def GetADCRSADFAAreaData():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"reason": "incorrect value"}), 400

        ext_ent_id = data.get("external_entity_id")
        
        # Validation
        if not ext_ent_id:
            return jsonify({"reason": "incorrect value"}), 400

        # Optional: Validate numeric day
        try:
            ext_ent_id = int(ext_ent_id)
        except:
            return jsonify({"reason": "incorrect value"}), 400

        # -----------------------------
        # Generate Response Data
        # -----------------------------
        response_data = {
            "action_flag" : 1,
            "area_name"  : "abc",
            "adfa_classification" : "xyz",
            "maximum_height" : "123",
            "shape_type" : "H"
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"reason": "internal_server_error"}), 500


# ---------------------------------------
# RUN SERVER
# ---------------------------------------
if __name__ == '__main__':
    app.run(debug=True)



# -----------------------------------------
# 404 Handler (Custom)
# -----------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "reason": "resource method is not available"
    }), 404


# -----------------------------------------
# 405 Handler (Method Not Allowed)
# -----------------------------------------
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "reason": "resource method is not available"
    }), 404


# -----------------------------------------
# Run Server
# -----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)