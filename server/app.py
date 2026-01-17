from flask import Flask, request, session, jsonify, make_response

app = Flask(__name__)
app.json.compact = False  # Ensures pretty JSON output

# Secret key for signing the session cookie (keep this secure!)
app.secret_key = b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    """
    Set default session values if they don't exist.
    Return current session data and cookies.
    """
    # Set default session values
    session.setdefault("hello", "World")
    session.setdefault("goodnight", "Moon")

    # Ensure the requested key exists in the session
    if key not in session:
        return make_response(
            jsonify({"error": f"Session key '{key}' not found"}), 404
        )

    # Build response with session and cookies info
    response = make_response(
        jsonify({
            'session': {
                'session_key': key,
                'session_value': session[key],
                'session_accessed': session.accessed,
            },
            'cookies': [{cookie: request.cookies[cookie]} for cookie in request.cookies],
        }),
        200
    )

    # Set a custom cookie
    response.set_cookie('mouse', 'Cookie', httponly=True, samesite='Lax')

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)