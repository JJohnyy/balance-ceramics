from django.shortcuts import get_object_or_404

from profducts.modes import Mugs


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    mugs = Mugs.objects.all()

    mugs_slug_list = []

    for mug in mugs:
        mugs_slug_list.append(mug.slug_name)

        for item_slug, quantity in bag.items():

            if item_slug in mugs_slug_list:
                product = get_object_or_404(Mugs, slug_name=item_slug)
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_slug': item_slug,
                    'quantity': quantity,
                    'product': product,
                })

    grand_total = total

    contexts = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return contexts

