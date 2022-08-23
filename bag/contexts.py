
from django.shortcuts import get_object_or_404

from products.models import Mugs


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    mugs = Mugs.objects.all()

   
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):

            product = get_object_or_404(Mugs, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

    grand_total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context
