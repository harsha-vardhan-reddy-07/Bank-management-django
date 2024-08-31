from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('admin-register', views.bank_register, name='register'),
    
    
    path('home/', views.loadHome, name='loadHome'),
    path('home/<str:id>', views.home, name='home'),
    path('deposits/', views.loadDeposit, name='loadDeposit'),
    path('deposits/<str:id>', views.deposit, name='deposit'),
    path('loans/', views.loadLoan, name='loadLoan'),
    path('loans/<str:id>', views.loan, name='loan'),
    path('transactions', views.loadTranasactions, name='loadTransactions'),
    path('transactions/<str:id>', views.transactions, name='transactions'),
    
    path('repay-loan/<str:id>/<int:amount>', views.repayLoan, name='repayLoan'),
     
    path('adminHome', views.adminHome, name='adminHome'),
    path('adminDeposits', views.adminDeposits, name='adminDeposits'),
    path('adminLoans', views.adminLoans, name='adminLoans'),
    path('adminTransactions', views.adminTransactions, name='adminTransactions'),
    path('allUsers', views.allUsers, name='adminUsers'),
    
    path('approve-loan/<str:id>', views.approveLoan, name='adminUsers'),
    path('reject-loan/<str:id>', views.rejectLoan, name='adminUsers'),
    
    
]
