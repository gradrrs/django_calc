# calculator/views.py
from django.shortcuts import render
from datetime import datetime

operations_history = []

def calculator_view(request):
    context = {
        'result': None,
        'error': None,
        'num1': '',
        'num2': '',
        'operation': '+'
    }
    
    return render(request, 'calculator/calculator.html', context)


def calculate(request):
    if request.method == 'POST':
        try:
            num1 = request.POST.get('num1', '')
            num2 = request.POST.get('num2', '')
            operation = request.POST.get('operation', '+')
            
            if not num1 or not num2:
                raise ValueError("Оба поля должны быть заполнены")
            
            num1_float = float(num1)
            num2_float = float(num2)
            
            if operation == '+':
                result = num1_float + num2_float
            elif operation == '-':
                result = num1_float - num2_float
            elif operation == '*':
                result = num1_float * num2_float
            elif operation == '/':
                if num2_float == 0:
                    raise ZeroDivisionError("Деление на ноль невозможно")
                result = num1_float / num2_float
            else:
                raise ValueError("Неизвестная операция")
            
            history_entry = {
                'num1': num1_float,
                'num2': num2_float,
                'operation': operation,
                'result': result,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            operations_history.append(history_entry)
            
            if len(operations_history) > 10:
                operations_history.pop(0)
            
            context = {
                'result': result,
                'num1': num1,
                'num2': num2,
                'operation': operation,
                'error': None
            }
            
        except ValueError as e:
            context = {
                'result': None,
                'num1': num1,
                'num2': num2,
                'operation': operation,
                'error': str(e)
            }
        except ZeroDivisionError as e:
            context = {
                'result': None,
                'num1': num1,
                'num2': num2,
                'operation': operation,
                'error': str(e)
            }
        except Exception as e:
            context = {
                'result': None,
                'num1': num1,
                'num2': num2,
                'operation': operation,
                'error': f"Ошибка: {str(e)}"
            }
    else:
        context = {
            'result': None,
            'num1': '',
            'num2': '',
            'operation': '+',
            'error': None
        }
    
    return render(request, 'calculator/calculator.html', context)


def history_view(request):
    recent_history = list(reversed(operations_history[-10:]))
    
    context = {
        'history': recent_history
    }
    
    return render(request, 'calculator/history.html', context)