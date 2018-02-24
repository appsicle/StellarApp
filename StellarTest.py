from flask import Flask, redirect
from flask import render_template, request
from stellar_base.keypair import Keypair
from stellar_base.builder import Builder

import json

#running on http://127.0.0.1:5000/
app = Flask(__name__)

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
        print(s['_links'])
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

if __name__ == '__main__':
    #site keypair
    SITE_ADDRESS = 'GAQINBPLEN4IA2CII7ZC6ECW4577WYCEX7RRRMZICAQEVDC3RVHUQOB5'
    SITE_SEED = 'SBMXXBHTEUHGX3BLEALIWD2LPQA4Y2AF6ZE75BR5TNJPUYFYNJXSOZ66'
    #member keypair
    MEMBER_ADDRESS = 'GDGIN33YFU4XJWJQMFIAVZVKI55T6ICW5CMOOPUS44JSCPNJ22GTQOOV'
    MEMBER_SEED = 'SCLGJI7HMIULRNC72KSBKGCSPZLY3UKW6VPYN5VNIZYYCNTMPLML75GM'

    app.run(debug=True)
