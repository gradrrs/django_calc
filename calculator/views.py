from django.shortcuts import render, redirect
from django.utils import timezone
import math
from django.contrib import messages

def calculator_view(request):
    return render(request, 'calculator/calculator.html')

def calculate(request):
    if request.method == 'POST':
        try:
            num1 = request.POST.get('num1', '').strip()
            operation = request.POST.get('operation', '+')
            
            if '.' in num1:
                num1_val = float(num1)
            else:
                num1_val = int(num1)
            
            result = None
            num2_val = None
            
            if operation in ['sqrt', 'pow']:
                if operation == 'sqrt':
                    if num1_val < 0:
                        raise ValueError("Квадратный корень из отрицательного числа невозможен")
                    result = math.sqrt(num1_val)
                    calculation_display = f"√{num1} = {result:.6f}"
                elif operation == 'pow':
                    result = num1_val ** 2
                    calculation_display = f"{num1}² = {result:.6f}"
            else:
                num2 = request.POST.get('num2', '').strip()
                if not num2:
                    raise ValueError("Введите второе число")
                    
                if '.' in num2:
                    num2_val = float(num2)
                else:
                    num2_val = int(num2)
                
                if operation == '+':
                    result = num1_val + num2_val
                elif operation == '-':
                    result = num1_val - num2_val
                elif operation == '*':
                    result = num1_val * num2_val
                elif operation == '/':
                    if num2_val == 0:
                        raise ZeroDivisionError("Деление на ноль невозможно")
                    result = num1_val / num2_val
                
                calculation_display = f"{num1} {operation} {num2} = {result:.6f}"
            
            if result is not None:
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                elif isinstance(result, float):
                    result = round(result, 6)
            
            history = request.session.get('calculation_history', [])
            history_entry = {
                'num1': num1,
                'operation': operation,
                'num2': str(num2_val) if num2_val is not None else '',
                'result': str(result),
                'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                'display': calculation_display
            }
            history.insert(0, history_entry)  
            request.session['calculation_history'] = history[:50]
            request.session.modified = True
            
            context = {
                'num1': num1,
                'operation': operation,
                'num2': str(num2_val) if num2_val is not None else '',
                'result': result,
                'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            return render(request, 'calculator/calculator.html', context)
            
        except ValueError as e:
            error_message = str(e)
            if "could not convert string to float" in error_message.lower():
                error_message = "Пожалуйста, введите корректные числа"
        except ZeroDivisionError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"Произошла ошибка: {str(e)}"
        
        return render(request, 'calculator/calculator.html', {
            'error': error_message,
            'num1': request.POST.get('num1', ''),
            'operation': request.POST.get('operation', '+'),
            'num2': request.POST.get('num2', ''),
        })
    
    return redirect('calculator')

def history_view(request):
    history = request.session.get('calculation_history', [])
    
    if request.method == 'POST' and 'clear_history' in request.POST:
        request.session['calculation_history'] = []
        request.session.modified = True
        messages.success(request, "История операций очищена")
        return redirect('history')
    
    return render(request, 'calculator/history.html', {
        'history': history
    })

def clear_history(request):
    if request.method == 'POST':
        request.session['calculation_history'] = []
        request.session.modified = True
        messages.success(request, "История операций очищена")
    return redirect('history')