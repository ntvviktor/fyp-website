from webapp import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(port=8000, debug=True)
    # app.run(host="192.168.18.68", port=8000, debug=True)
