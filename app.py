from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Load credentials and authorize
creds = Credentials.from_service_account_file("config/iamadinkra-ff3a4-b9c9461c40ec.json")
client = gspread.authorize(creds)

# Open Google Sheet
SHEET_NAME = "Test Spreadsheet api "
worksheet = client.open(SHEET_NAME).sheet1

@app.route("/", methods=["GET"])
def home():
    return "Wedding RSVP System"

@app.route("/rsvp", methods=["POST"])
def rsvp():
    data = request.json
    guest_code = data.get("code")
    rsvp_status = data.get("status")  # Should be "Yes" or "No"

    if not guest_code or not rsvp_status:
        return jsonify({"error": "Code and RSVP status are required"}), 400

    all_records = worksheet.get_all_records()

    for i, record in enumerate(all_records, start=2):  # Start at row 2 (after headers)
        if str(record["Code"]) == guest_code:
            worksheet.update_cell(i, record.keys().index("RSVP Status") + 1, rsvp_status)
            message = "Thank you for confirming! We can't wait to see you." if rsvp_status == "Yes" else "Sorry to see you go. Maybe next time!"
            return jsonify({"message": message})

    return jsonify({"error": "Guest not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
