from app.main import app
from socket import gethostname

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
	    app.run(debug=False)
