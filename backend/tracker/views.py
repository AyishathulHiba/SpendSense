from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Expense, Income, UserProfile, Category
from .serializers import ExpenseSerializer, IncomeSerializer, CategorySerializer
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from datetime import datetime

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    full_name = data.get('full_name')
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password or not confirm_password:
        return Response({'error': 'Username and password are required'}, status=400)

    if password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if email and User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=full_name if full_name else ""
    )

    UserProfile.objects.create(
        user=user,
        phone=phone
    )

    return Response({'message': f'{username}, registered successfully!'}, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful', 'token': token.key, 'username': username})
    else:
        return Response({'error': 'Invalid username or password'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_expense(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_income(request):
    serializer = IncomeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_incomes(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    serializer = IncomeSerializer(incomes, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk, user=request.user)
    except Expense.DoesNotExist:
        return Response({'error': 'Expense not found'}, status=404)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    serializer = ExpenseSerializer(expense, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk, user=request.user)
        expense.delete()
        return Response({'message': 'Expense deleted successfully'})
    except Expense.DoesNotExist:
        return Response({'error': 'Expense not found'}, status=404)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_income(request, pk):
    try:
        income = Income.objects.get(pk=pk, user=request.user)
    except Income.DoesNotExist:
        return Response({'error': 'Income not found'}, status=404)

    if request.method == 'GET':
        serializer = IncomeSerializer(income)
        return Response(serializer.data)

    serializer = IncomeSerializer(income, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_income(request, pk):
    try:
        income = Income.objects.get(pk=pk, user=request.user)
        income.delete()
        return Response({'message': 'Income deleted successfully'})
    except Income.DoesNotExist:
        return Response({'error': 'Income not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_categories(request):
    categories = Category.objects.filter(user=request.user)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk, user=request.user)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk, user=request.user)
        category.delete()
        return Response({'message': 'Category deleted successfully'})
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expense_categories(request):
    categories = Category.objects.filter(user=request.user, type='Expense')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_income_categories(request):
    categories = Category.objects.filter(user=request.user, type='Income')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_summary(request):
    today = datetime.today()
    income_total = Income.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    expense_total = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    return Response({'income': income_total, 'expense': expense_total})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_summary(request):
    user = request.user

    expense_data = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))
    income_data = Income.objects.filter(user=user).values('category').annotate(total=Sum('amount'))

    return Response({
        'expenses': expense_data,
        'incomes': income_data
    })


def perform_create(self, serializer):
    serializer.save(user=self.request.user)
