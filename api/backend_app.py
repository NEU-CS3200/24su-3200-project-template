from backend.rest_entry import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True enables hot reloading when code changes.
    # The app is bound to 0.0.0.0 so it's reachable from outside the container.
    # See docker-compose.yaml for the host port it's mapped to.
    app.run(debug=True, host='0.0.0.0', port=4000)
