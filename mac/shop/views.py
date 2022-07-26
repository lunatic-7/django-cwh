import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate

# Create your views here.
def index(request):
    products = Product.objects.all()
    home = []
    tech = []
    for _ in products:
        if _.category == "home":
            home.append(_)
        elif _.category == "tech":
            tech.append(_)
    params = {'tech': tech, 'home': home}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return True only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get("search")
    prodtemp = Product.objects.all()

    home = []
    tech = []
    prod = [item for item in prodtemp if searchMatch(query, item)]
    print(prod)
    for _ in prod:
        if _.category == "home":
            home.append(_)
        elif _.category == "tech":
            tech.append(_)
    if len(prod) != 0:
        params = {'tech': tech, 'home': home}
    else:
        params = {}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        desc = request.POST.get("desc", "")

        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')
    

def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get("orderId", "")
        email = request.POST.get("email", "")
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(items_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, "time": item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except:
            return HttpResponse("{}")

    return render(request, 'shop/tracker.html')

def prodView(request, myid):
    # Fetch the product using it's id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get("itemsJson", "")
        amount = request.POST.get("amount", "")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address1", "") + " " + request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")

        order = Orders(items_json = items_json, name=name, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code, amount=amount)
        order.save()
        update = OrderUpdate(items_id = order.order_id, update_desc="The Order Has Been Placed!")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')

