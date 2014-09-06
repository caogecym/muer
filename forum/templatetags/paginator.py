from django import template

register = template.Library()

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    cur_idx = context['posts'].number
    ttl_idx = context['posts'].paginator.num_pages

    startPage = max(cur_idx - adjacent_pages, 1)
    if startPage <= 3:
        startPage = 1
    endPage = cur_idx + adjacent_pages + 1

    if endPage >= ttl_idx - 1:
        endPage = ttl_idx + 1
    page_numbers = [n for n in range(startPage, endPage) if n > 0 and n <= ttl_idx]

    has_next = context['posts'].has_next()
    has_previous = context['posts'].has_previous()
    next = None
    previous = None
    if has_next:
        next = context['posts'].next_page_number()
    if has_previous:
        previous = context['posts'].previous_page_number()

    return {
        'page': cur_idx,
        'pages': ttl_idx,
        'page_numbers': page_numbers,
        'next': next,
        'previous': previous,
        'has_next': has_next,
        'has_previous': has_previous,
        'show_first': 1 not in page_numbers,
        'show_last': ttl_idx not in page_numbers,
    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)
