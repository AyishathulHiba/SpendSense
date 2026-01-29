from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_api, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('expenses/', views.list_expenses, name='list_expenses'),
    path('add-income/', views.add_income, name='add_income'),
    path('list-incomes/', views.list_incomes, name='list_incomes'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('update-expense/<int:pk>/', views.update_expense, name='update_expense'),
    path('delete-expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('update-income/<int:pk>/', views.update_income, name='update_income'),
    path('delete-income/<int:pk>/', views.delete_income, name='delete_income'),
    path('categories/', views.list_categories, name='list_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('update-category/<int:pk>/', views.update_category, name='update_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('expense-categories/', views.get_expense_categories, name='expense-categories'),
    path('income-categories/', views.get_income_categories, name='income-categories'),
    path('reports/monthly-summary/', views.monthly_summary, name='monthly_summary'),
    path('reports/category-summary/', views.category_summary, name='category_summary'),
    # path('savings-insights/', views.savings_insights, name='savings-insights'),

]
