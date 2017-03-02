import sys

sys.path.append('/WhatAClass')
sys.path.append('/WhatAClass/WhatAClass')

from WhatAClass.app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='80')

