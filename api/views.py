from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, AdminRegisterForm, TransferForm, DepositForm, LoanForm
from .models import users_collection, loans_collection, transactions_collection, deposits_collection, banks_collection
import bson
from datetime import datetime, timedelta

def landing(request):
    return render(request, 'landing.html')


def login(request):
    error=''
    data = {}
    isLogged = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                data = users_collection.find_one({'email': email})
                if data.get('password') == password:
                    data['userId'] = str(data['_id'])
                    isLogged = True
                
                else:
                    form = LoginForm()
                    error = 'Wrong credientials. Please try again.'
                    
            except:
                form = LoginForm()
                error = 'User not found!! Please try again.'
        else:
            form = LoginForm()
            error = 'Wrong credientials. Please try again.'
    else:
        form = LoginForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'login.html', context)


def register(request):
    error=''
    data = {}
    isLogged = False
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            IFSC = {'hyderabad': 'SB007HYD25', 
                    'bangalore': 'SB007BLR30',
                    'chennai': 'SB007CNI99', 
                    'mumbai': 'SB007MBI12', 
                    'tirupati': 'SB007TPTY05',
                    'vizag': 'SB007VZG229',
                    'pune': 'SB007PN77', 
                    'delhi': 'SB007DLI09', 
                    'kochi': 'SB007KCI540',
                    'Venkatagiri': 'SB007VGR313',  
                }
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            homeBranch = form.cleaned_data['homeBranch']
            userType = "user"
            balance = 0
            IFSCCode = IFSC[homeBranch]
            
            
            user = {"username": username, "email": email, "password": password, "userType": userType, "homeBranch": homeBranch, "balance": balance, "IFSCCode": IFSCCode}
            result = users_collection.insert_one(user)
            isLogged = True
            data = {
            'userId': str(result.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'userType': userType,
            'homeBranch': homeBranch,
            'balance': balance,
            'IFSCCode': IFSCCode
            }
            
        else:
            form = RegisterForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = RegisterForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'register.html', context)


def bank_register(request):
    error=''
    data = {}
    isLogged = False
    
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            userType = "admin"
            
            user = {"username": username, "email": email, "password": password, "userType": userType}
            result = users_collection.insert_one(user)
            isLogged = True
            data = {
            'userId': str(result.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'userType': userType,
            }
            
        else:
            form = AdminRegisterForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = AdminRegisterForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'bank-register.html', context)


def loadHome(request):
    return render(request, 'user/loadHome.html')

def home(request, id):
    user = users_collection.find_one({'_id': bson.ObjectId(id)})
    user['id'] = str(user['_id'])
    error=''
    paymentSuccess = False
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            
            if user['balance'] < form.cleaned_data['amount']:
                error = 'Insufficient balance. Please try again.'
                form = TransferForm(initial={'senderId': user['id'], 'senderName': user['username'] })
                context = {'form': form, 'user': user, 'paymentSuccess': paymentSuccess, 'error': error}
                return render(request, 'user/home.html', context)
            
            receiver = users_collection.find_one({'_id': bson.ObjectId(form.cleaned_data['receiverId'])})
            
            if receiver == None:
                error = 'Receiver not found. Please try again.'
                form = TransferForm(initial={'senderId': user['id'], 'senderName': user['username'] })
                context = {'form': form, 'user': user, 'paymentSuccess': paymentSuccess, 'error': error}
                return render(request, 'user/home.html', context)
            
            
            user['balance'] -= form.cleaned_data['amount']
            receiver['balance'] += form.cleaned_data['amount']
            
            users_collection.update_one({'_id': bson.ObjectId(user['id'])}, {'$set': {'balance': user['balance']}})
            users_collection.update_one({'_id': bson.ObjectId(receiver['_id'])}, {'$set': {'balance': receiver['balance']}})
            
            senderId = form.cleaned_data['senderId']
            senderName = form.cleaned_data['senderName']
            remarks = form.cleaned_data['remarks']
            receiverId = form.cleaned_data['receiverId']
            receiverIFSC = form.cleaned_data['receiverIFSC']
            receiverName = receiver['username']
            amount = form.cleaned_data['amount']
            paymentMethod = form.cleaned_data['paymentMethod']
            time = str(datetime.now())

            
            transaction = {"senderId": senderId, "senderName": senderName, "remarks": remarks, "receiverId": receiverId, "receiverIFSC": receiverIFSC, "receiverName": receiverName, "amount": amount, "paymentMethod": paymentMethod, "time": time}
            result = transactions_collection.insert_one(transaction)
            paymentSuccess = True
            
        else:
            form = TransferForm(initial={'senderId': user['id'], 'senderName': user['username'] })
            error = 'Invalid form data. Please try again.'
    else:
        form = TransferForm(initial={'senderId': user['id'], 'senderName': user['username'] })
    
    context = {'form': form, 'user': user, 'paymentSuccess': paymentSuccess, 'error': error}
    
    return render(request, 'user/home.html', context)


def loadDeposit(request):
    return render(request, 'user/loadDeposits.html')


def deposit(request, id):
    user = users_collection.find_one({'_id': bson.ObjectId(id)})
    user['id'] = str(user['_id'])
    error=''
    success = False
    deposits = [deposit for deposit in  deposits_collection.find({'customerId': user['id']})]
    for deposit in deposits:
        deposit['id'] = str(deposit['_id'])
        
    deposits.reverse()
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            
            user['balance'] -= form.cleaned_data['amount']
            
            users_collection.update_one({'_id': bson.ObjectId(user['id'])}, {'$set': {'balance': user['balance']}})

  
            depositName = form.cleaned_data['depositName']
            customerId = form.cleaned_data['customerId']
            customerName = form.cleaned_data['customerName']
            nomineeName = form.cleaned_data['nomineeName']
            nomineeAge = form.cleaned_data['nomineeAge']
            amount = form.cleaned_data['amount']
            duration = form.cleaned_data['duration']
            createdDate = str(datetime.now())
            mature_date1 = datetime.now() + timedelta(days= duration * 30)
            matureDate = str(mature_date1.strftime('%Y-%m-%d'))
            
            data = {"depositName": depositName, "customerId": customerId, "customerName": customerName, "nomineeName": nomineeName, "nomineeAge": nomineeAge, "amount": amount, "duration": duration, "createdDate": createdDate, "matureDate": matureDate}
            result = deposits_collection.insert_one(data)
            
            success = True
            
        else:
            form = DepositForm(initial={'customerId': user['id'], 'customerName': user['username'] })
            error = 'Invalid form data. Please try again.'
    else:
        form = DepositForm(initial={'customerId': user['id'], 'customerName': user['username'] })
    
    context = {'form': form, 'user': user, 'deposits': deposits, 'error': error, 'success': success}
    
    return render(request, 'user/deposits.html', context)

def loadLoan(request):
    return render(request, 'user/loadLoans.html')


def loan(request, id):
    user = users_collection.find_one({'_id': bson.ObjectId(id)})
    user['id'] = str(user['_id'])
    error=''
    success = False
    loans = [loan for loan in  loans_collection.find({'customerId': user['id']})]
    for loan in loans:
        loan['id'] = str(loan['_id'])
        
    loans.reverse()
    
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            
            loanType = form.cleaned_data['loanType']
            customerId = form.cleaned_data['customerId']
            customerName = form.cleaned_data['customerName']
            nomineeName = form.cleaned_data['nomineeName']
            nomineeAge = form.cleaned_data['nomineeAge']
            duration = form.cleaned_data['duration']
            loanAmount = form.cleaned_data['loanAmount']
            balance = form.cleaned_data['loanAmount']
            loanStatus = 'pending'
            createdDate = str(datetime.now().strftime('%Y-%m-%d'))
            endDate = ""
            
            data = {"loanType": loanType, "customerId": customerId, "customerName": customerName, "nomineeName": nomineeName, "nomineeAge": nomineeAge, "duration": duration, "loanAmount": loanAmount, "balance": balance, "loanStatus": loanStatus, "createdDate": createdDate, "endDate": endDate}
            result = loans_collection.insert_one(data)
            
            success = True
            
        else:
            form = LoanForm(initial={'customerId': user['id'], 'customerName': user['username'] })
            error = 'Invalid form data. Please try again.'
    else:
        form = LoanForm(initial={'customerId': user['id'], 'customerName': user['username'] })
    
    context = {'form': form, 'user': user, 'loans': loans, 'error': error, 'success': success}
    
    return render(request, 'user/loans.html', context)


def repayLoan(request, id, amount):
    success = False
    try:
        
        loan = loans_collection.find_one({'_id': bson.ObjectId(id)})
        loan['id'] = str(loan['_id'])
        
        if loan['balance'] == amount:
            loan['loanStatus'] = 'completed'
            loan['balance'] = 0
            loans_collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'balance': loan['balance'], 'loanStatus': 'completed'}})
        else:
            loan['balance'] -= amount
            loans_collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'balance': loan['balance']}})
        
        user = users_collection.find_one({'_id': bson.ObjectId(loan['customerId'])})
        user['balance'] -= amount
        
        users_collection.update_one({'_id': bson.ObjectId(loan['customerId'])}, {'$set': {'balance': user['balance']}})
        
        success = True
    except:
       success = False 
    return render(request, 'user/repayLoan.html', {'success': success})


def loadTranasactions(request):
    return render(request, 'user/loadTransactions.html')


def transactions(request, id):
    transactions = transactions_collection.find({'senderId': id})
    return render(request, 'user/transactions.html', {'transactions': transactions, 'userId': id})


def adminHome(request):
    users = len([user for user in users_collection.find()])
    loans = len([loan for loan in loans_collection.find()])
    deposits = len([deposit for deposit in deposits_collection.find()])
    transactions = len([transaction for transaction in transactions_collection.find()])
    return render(request, 'admin/home.html', {'users': users, 'loans': loans, 'deposits': deposits, 'transactions': transactions})

def adminDeposits(request):
    deposits = [deposit for deposit in deposits_collection.find()]
    for deposit in deposits:
        deposit['id'] = str(deposit['_id'])
    deposits.reverse()
    return render(request, 'admin/allDeposits.html', {'deposits': deposits})

def adminLoans(request):
    loans = [loan for loan in loans_collection.find()]
    for loan in loans:
        loan['id'] = str(loan['_id'])
        loan['createdDate'] = loan['createdDate'][0:10]
    loans.reverse()
    
    loanRequests = [loan for loan in loans_collection.find({'loanStatus': 'pending'})]
    for loan in loanRequests:
        loan['id'] = str(loan['_id'])
        loan['createdDate'] = loan['createdDate'][0:10]
    loanRequests.reverse()
    return render(request, 'admin/allLoans.html', {'loans': loans, 'loanRequests': loanRequests})


def approveLoan(request, id):
    success = False
    try:
        loan = loans_collection.find_one({'_id': bson.ObjectId(id)})
        loan['id'] = str(loan['_id'])
        loan['loanStatus'] = 'approved'
        endDate = datetime.now() + timedelta(days= loan['duration'] * 30)
        loan['endDate'] = str(endDate.strftime('%Y-%m-%d'))
        loans_collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'loanStatus': 'approved', 'endDate': loan['endDate']}})
        
        user = users_collection.find_one({'_id': bson.ObjectId(loan['customerId'])})
        user['balance'] += loan['loanAmount']
        
        users_collection.update_one({'_id': bson.ObjectId(loan['customerId'])}, {'$inc': {'balance': user['balance']}})
        
        success = True
    except:
       success = False 
    return render(request, 'admin/approveLoan.html', {'success': success})

def rejectLoan(request, id):
    success = False
    try:
        loan = loans_collection.find_one({'_id': bson.ObjectId(id)})
        loan['id'] = str(loan['_id'])
        loan['loanStatus'] = 'rejected'
        loans_collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'loanStatus': 'declined'}})
        success = True
    except:
       success = False 
    return render(request, 'admin/rejectLoan.html', {'success': success})


def adminTransactions(request):
    transactions = [transaction for transaction in transactions_collection.find()]
    for transaction in transactions:
        transaction['id'] = str(transaction['_id'])
    transactions.reverse()
    return render(request, 'admin/allTransactions.html', {'transactions': transactions})


def allUsers(request):
    users = [user for user in users_collection.find({'userType': 'user'})]
    for user in users:
        user['id'] = str(user['_id'])
    return render(request, 'admin/allUsers.html', {'users': users})
