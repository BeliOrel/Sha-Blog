from shablog import create_app

app = create_app()

# if we don't want to use environment variables
# for a debug mode, we can also write
if __name__ == '__main__':
    app.run(debug=True)
