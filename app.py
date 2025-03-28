from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['GET', 'POST'])
def run_bot():
    if request.method == 'GET':
        return "✅ Bot is alive", 200

    try:
        # Run your calendly_bot.py script
        subprocess.run(["python3", "calendly_bot.py"], check=True)
        return jsonify({"status": "success", "message": "Calendly bot executed!"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
