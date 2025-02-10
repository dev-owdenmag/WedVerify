from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Load the service account credentials
creds = Credentials.from_service_account_file('config/iamadinkra-ff3a4-0dbd29adaaf9.json', scopes=SCOPES)

# Authorize the client
client = gspread.authorize(creds)

# Open the spreadsheet
SHEET_NAME = "J&O Wedding Guest Data 2025"
worksheet = client.open(SHEET_NAME).sheet1

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/rsvp', methods=['POST'])
def rsvp():
    data = request.json
    guest_code = data.get("code")
    rsvp_status = data.get("status") #Should be Confirmed or Dclined

    if not guest_code:
        return jsonify({"error": "Entet a valid rsvp code"}), 400
    
    all_records = worksheet.get_all_records()

    for i, record in enumerate(all_records, start=2):
        if str (record["Code"]) == guest_code:
            worksheet.update_cell(i, record.keys().index("RSVP Status") + 1, rsvp_status)
            message = "Thank you for confirming! We can't wait to see you." if rsvp_status == "Yes" else "We are sorry to see you go. Maybe next time!"
            return jsonify({"message": message})
        
        return jsonify({"error": "Invalid RSVP code"}), 404
    
    if __name__ == '__main__':
        app.run(debug=True)