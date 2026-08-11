from flask import Flask, request, jsonify

app = Flask(__name__)

# Divide and Conquer Min-Max Algorithm
def find_min_max(arr, low, high):
    # Base case: one element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]

    # Recursive case
    mid = (low + high) // 2
    left_min, left_max = find_min_max(arr, low, mid)
    right_min, right_max = find_min_max(arr, mid + 1, high)

    overall_min = min(left_min, right_min)
    overall_max = max(left_max, right_max)

    return overall_min, overall_max


@app.route("/")
def home():
    return "⚡ Power Grid Monitoring System API is running!"


@app.route("/minmax", methods=["POST"])
def minmax():
    """
    Expects JSON input:
    {
        "readings": [list of voltage readings]
    }
    """
    data = request.get_json()
    readings = data.get("readings", [])

    if not readings:
        return jsonify({"error": "No readings provided"}), 400

    min_val, max_val = find_min_max(readings, 0, len(readings) - 1)

    return jsonify({
        "min_voltage": min_val,
        "max_voltage": max_val,
        "total_readings": len(readings)
    })


if __name__ == "__main__":
    # Render will run this with gunicorn, but for local testing:
    app.run(host="0.0.0.0", port=5000, debug=True)
