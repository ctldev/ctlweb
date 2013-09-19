#vim: set fileencoding=utf-8

def generate_page_buttons(prefix, page_count, css_class, page, button_range):
    """generate buttons for pagination"""
    buttons = []
    buttons.append(_generate_button(prefix, "first", css_class, "|&laquo;",
            disabled=(page==1)))
    buttons.append(_generate_button(prefix, "prev", css_class, "&laquo;",
            disabled=(page==1)))

    start = page - (button_range + 1)
    end = page + button_range
    if start < 0:
        start = 0
    if end > page_count:
        end = page_count
    for i in range(start, end):
        buttons.append(_generate_button(prefix, i+1, css_class,
            active=((i+1)==page)))

    buttons.append(_generate_button(prefix, "next", css_class, "&raquo;",
        disabled=(page==page_count)))
    buttons.append(_generate_button(prefix, "last", css_class, "&raquo;|",
        disabled=(page==page_count)))
    return buttons

def _generate_button(prefix, page, css_class, value=None, disabled=False,
        active=False):
    """helper to generate th pagination-buttons"""
    if value == None:
        value = page
    if disabled:
        button = '<li class="disabled">'
    elif active:
        button = '<li class="active">'
    else:
        button = "<li>"
    button +=      """ <a href="javascript:void(0)"
                      class="%s" id="%s%s" """ % (css_class, prefix, page)
    if not disabled and not active:
        button += 'onclick="loadXMLDoc($(this))"'
    button += ">%s</a></li>" % value
    return button
