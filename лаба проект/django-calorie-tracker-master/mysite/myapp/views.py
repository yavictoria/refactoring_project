"""Views for handling food consumption tracking."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Food, Consume

@login_required
def index(request):
    """Render homepage with food selection and consumption table."""
    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        try:
            consume_item = Food.objects.get(name=food_consumed)  # pylint: disable=no-member
            consume = Consume(user=request.user, food_consumed=consume_item)
            consume.save()
        except Food.DoesNotExist:  # pylint: disable=no-member
            return redirect('index')

    foods = Food.objects.all()  # pylint: disable=no-member
    consumed_food = Consume.objects.filter(user=request.user)  # pylint: disable=no-member

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})

@login_required
def delete_consume(request, consume_id):
    """Delete a food consumption record."""
    try:
        consumed_food = Consume.objects.get(id=consume_id)  # pylint: disable=no-member
    except Consume.DoesNotExist:  # pylint: disable=no-member
        return redirect('index')

    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'myapp/delete.html')
