from flask import Flask, request
import requests as http
import os

__client_id__ = "<your_client_id_here>"
__client_secret__ = os.getenv('CLIENT_SECRET')
__code_challenge__ = "51FaJvQFsiNdiFWIq2EMWUKeAqD47dqU_cHzJpfHl-Q"
__code_verifier__ = "c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646"
__scopes__ = { "openid", "shared" }
__redirect_url__ = "https://localhost:5001"

app = Flask(__name__)

@app.route("/")
def get_token():
    args = request.args
    code = args.get("code", default="", type=str)

    request_body = {
        "client_id": __client_id__,
        "client_secret": __client_secret__,
        "code_verifier": __code_verifier__,
        "scope":" ".join(__scopes__),
        "grant_type": "authorization_code",
        "redirect_uri": __redirect_url__,
        "code": code
    }
    auth_result = http.post("https://auth.dodois.io/connect/token", data=request_body)

    access_token = auth_result.json()["access_token"]
    save_token(access_token)

    return '', 204

def save_token(token):
    print(token)
    #do what you need

def show_sign_in_url(clientId, scopes, redirect_url, code_challenge):
    print("Open this link in browser:")
    url = f'https://auth.dodois.io/connect/authorize?client_id={clientId}&scope={" ".join(scopes)}&response_type=code&redirect_uri={redirect_url}&code_challenge={code_challenge}&code_challenge_method=S256'
    print(url)

if __name__ == "__main__":
    show_sign_in_url(__client_id__, __scopes__, __redirect_url__, __code_challenge__)
    app.run(host="localhost", port=5001, ssl_context='adhoc')

