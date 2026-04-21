from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define the path for the counter file to store the data in Docker Volume
COUNTER_FILE = "/data/counter.txt"

def read_counter():
    """
    Reads and returns the current counter value from the file.
    If the file doesn't exist, it return 0.
    
    Returns:
        int: The current counter value.
    """
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    else:
        return 0

def update_counter(counter):
    """
    Updates the counter file with the new counter value.
    
    Args:
        counter (int): The new counter value to write to the file.
    """
    with open(COUNTER_FILE, "w") as f:
        f.write(str(counter))

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    counter = read_counter()
    if request.method == 'POST':
        counter += 1
        update_counter(counter)
        message = f"Count Updated!"
    else:
        message = f"Welcome to the Dashboard"

    # This is "Template" HTML
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f9; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }}
                h1 {{ color: #333; }}
                .count {{ font-size: 48px; color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>{message}</h1>
                <p>Total POST Requests:</p>
                <div class="count">{counter}</div>
            </div>
        </body>
    </html>
    """

@app.route('/health', methods=['GET'])
def health_check():
    """
    Performs a simple health check of the application.
    It tries to read the counter file as a basic check.
    
    Returns:
        tuple: A JSON response indicating the health status and the HTTP status code.
    """
    try:
        # Basic health check: Ensure the counter file is accessible.
        read_counter()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        # Return an unhealthy status if any error occurs, e.g., file access issues.
        return jsonify({"status": "unhealthy", "reason": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app with binding to all interfaces on port 8080.
    # Debug mode is turned off for production use.
    app.run(host='0.0.0.0', port=8080, debug=False)
