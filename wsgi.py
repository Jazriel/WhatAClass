from WhatAClass.app import create_app_and_db

application = create_app_and_db()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='80')
