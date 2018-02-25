from flask import Flask, redirect
from stellar_base.keypair import Keypair
from stellar_base.builder import Builder

import urllib.parse
import urllib.request
import json

#running on http://127.0.0.1:5000/
app = Flask(__name__)

@app.route('/') #home page
def index():
    return '''
<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
        <h1>
            <img src = https://themerkle.com/wp-content/uploads/stellar-logo.png>
        </h1>
        <div>
          <input type="button" value="PAY XLM" onclick="window.location='http://127.0.0.1:5000/pay'; " style="display: block; margin: 0 auto;">
        </div>
        <script type="text/javascript">
            document.getElementById("myButton").onclick = function () {
                location.href = "http://127.0.0.1:5000/pay";
            };
        </script>
    </body>
</html>

'''



@app.route("/gen_address")
def gen_address(): #generate a new keypair which will be send lumens using friendbot
    kp = Keypair.random()
    publickey = kp.address().decode()
    seed = kp.seed().decode()
    return json.dumps({'publickey': publickey, 'seed': seed})

def send_payment(amount, item, asset='XLM'):
    flag = False
    try:
        builder = Builder(secret=MEMBER_SEED) #send payment from member to site
        builder.append_payment_op(SITE_ADDRESS, amount, asset)
        builder.add_text_memo(item)
        builder.sign()
        s = builder.submit()
        global balance
        balance = calculate_balance(s)

        flag = True
    except Exception as e:
        print('Error', e)
    finally:
        return flag

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    result = False
    item = 'Buyer - Name1'
    amt = 10
    result = send_payment(amt, item)
    if result:
        return redirect('/thanks', code=302)
    else:
        return 'Invalid Transaction'

def calculate_balance(s):
    transaction_json = (s['_links'])
    account_dict = get_result(transaction_json['transaction']['href'])
    final_url = get_result(account_dict['_links']['account']['href'])
    balance = final_url['balances'][0]['balance']
    return balance

@app.route('/thanks')

def thanks():

    return 'Thanks for your payment. Your wallet now contains '+str(balance)+' xlm'

def get_result(url): #builds dict from url json
    response = None

    try:
        response = urllib.request.urlopen(url)
        return json.load(response)
    finally:
        if response != None:
            response.close()

if __name__ == '__main__':
    #site keypair
    SITE_ADDRESS = 'GAQINBPLEN4IA2CII7ZC6ECW4577WYCEX7RRRMZICAQEVDC3RVHUQOB5'
    SITE_SEED = 'SBMXXBHTEUHGX3BLEALIWD2LPQA4Y2AF6ZE75BR5TNJPUYFYNJXSOZ66'
    #member keypair
    MEMBER_ADDRESS = 'GDGIN33YFU4XJWJQMFIAVZVKI55T6ICW5CMOOPUS44JSCPNJ22GTQOOV'
    MEMBER_SEED = 'SCLGJI7HMIULRNC72KSBKGCSPZLY3UKW6VPYN5VNIZYYCNTMPLML75GM'
    app.run(debug=True)
