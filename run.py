#!flask/bin/python
from WhatAClass import create_app
if __name__ == '__main__':
    # import os
    # os.environ["WHATACLASS_CONFIG"] = "test_config.py"
    app = create_app()
    app.run(debug=True)
