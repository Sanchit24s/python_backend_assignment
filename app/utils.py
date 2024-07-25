from flask import url_for

def paginate_results(query, page, per_page):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    
    pagination_info = {
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page,
        'next': url_for('main.get_retreats', page=pagination.next_num) if pagination.has_next else None,
        'prev': url_for('main.get_retreats', page=pagination.prev_num) if pagination.has_prev else None
    }
    
    return items, pagination_info