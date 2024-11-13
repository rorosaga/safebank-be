from iebank_api import app
from flask import Flask, send_from_directory
import os

#app = Flask(__name__, static_folder='../safebank-fe/dist')
#db.init_app(app)

#@app.route('/<path:path>')
#def serve_vue_app(path):
 #   if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
  #      # go to a selected page I am choosing (like clientlogin)
   #     return send_from_directory(app.static_folder, path)
    #else:
     #   # go to main page
      #  return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)