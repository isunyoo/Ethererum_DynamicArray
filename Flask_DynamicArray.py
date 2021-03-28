import json, qrcode
import Pydenticon_Generator as icon
from web3 import Web3
from flask import Flask, render_template, request, redirect, flash, url_for

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
print("Web3 Connection: ", web3.isConnected())

# Function to account creation with images
def accountCreation(account_num):
    web3.eth.defaultAccount = web3.eth.accounts[account_num]
    print("Default Account:", web3.eth.defaultAccount)

    # Identicon Setup the padding(top, bottom, left, right) in pixels.
    padding = (10, 10, 10, 10)
    identicon_png = icon.generator.generate(web3.eth.defaultAccount, 20, 20, padding=padding, output_format="png")
    # Identicon can be easily saved to a file.
    f = open("static/images/%s.png" % (web3.eth.defaultAccount), "wb")
    f.write(identicon_png)
    f.close()
    #Creating an instance of QRCode image
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(web3.eth.defaultAccount)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('static/images/%s_qrcode.png' % (web3.eth.defaultAccount))

    return web3.eth.defaultAccount

# Opening JSON file and returns JSON object as a dictionary
with open('../build/contracts/DynamicArray.json') as f:  
  info_json = json.load(f)
ABI = info_json["abi"]
BYTECODE = info_json["bytecode"]
CONTRACT_ADDRESS = info_json["networks"]["4447"]["address"]
# print("abi file: ", ABI)  
# print("contract address: ", CONTRACT_ADDRESS)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI, bytecode=BYTECODE)

# Function to add data in dynamic array 
def newArrayValue(new_val):
    tx_hash = contract.functions.addData(new_val).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    message = "New Value "+str(new_val)+" has Added."
    flash(message, 'add')    

# Function to search data in dynamic array 
def searchArrayValue(new_val):        
    bool_data = contract.functions.search(new_val).call()
    print("\nSearch Data: %d is %s " % (new_val, bool_data))
    if bool_data is True:    
        message = "Search Value "+str(new_val)+" is Existed."
        flash(message, 'search')       
    if bool_data is False:
        message = "Search Value "+str(new_val)+" is Not Existed."
        flash(message, 'search')               

# Function to delete data in dynamic array 
def delArrayValue(new_val):
    bool_data = contract.functions.search(new_val).call()    
    if bool_data is True:
        tx_hash = contract.functions.delData(new_val).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)    
        message = "Deleting Value "+str(new_val)+" is Deleted."
        flash(message, 'delete') 
    if bool_data is False:
        message = "Deleting Value "+str(new_val)+" is Not Existed."
        flash(message, 'delete')

def getHelloFromBlockchain():
    hello_data = contract.functions.greet().call()
    print("\nGreeting Data: ", hello_data)
    return hello_data

def getLengthFromBlockchain():
    data_length = contract.functions.getLength().call() 
    print("\nData Length: ", data_length)
    return data_length

def getContentsFromBlockchain():
    data_contents = contract.functions.getData().call() 
    print("\nData Contents: ", data_contents)    
    return data_contents

def getSumFromBlockchain():
    data_sum = contract.functions.getSum().call() 
    print("\nData Sums: ", data_sum)
    return data_sum

# Flask http web display
app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = '12345'

@app.route('/', methods=['GET', 'POST'])
def index():
    # default_account = web3.eth.defaultAccount
    default_account = accountCreation(0)
    initial_hello = getHelloFromBlockchain()    
    initial_length = getLengthFromBlockchain()
    initial_contents = getContentsFromBlockchain()
    initial_sum = getSumFromBlockchain()    
    return render_template('index.html', value0=default_account, value1=initial_hello, value2=initial_length, value3=initial_contents, value4=initial_sum)

@app.route('/inputdata', methods=['POST'])
def newInput():
    stringValue = request.form['inputValue']
    newValue = int(stringValue)
    print("New Input Data :", newValue)
    newArrayValue(newValue)
    return redirect(url_for('index'))

@app.route('/searchdata', methods=['POST'])
def searchInput():
    stringValue = request.form['searchValue']
    newValue = int(stringValue)
    print("Search Input Data :", newValue)
    searchArrayValue(newValue)
    return redirect(url_for('index'))

@app.route('/deletedata', methods=['POST'])
def deleteInput():
    stringValue = request.form['deleteValue']
    newValue = int(stringValue)
    print("Delete Input Data :", newValue)
    delArrayValue(newValue)
    return redirect(url_for('index'))
    
# @app.route('/display', methods=['GET', 'POST'])
# def get_chain_data():    
#     output_result = getGreetingFromBlockchain()        
#     return render_template('display.html', value1=initial_result, value2=output_result)
   
if __name__ == '__main__':
    app.run(debug=True, port=5000)