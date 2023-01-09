from apiApp.models import landing_page

def layoutCreation(last_order,layout_type):
    if layout_type in ['left_image','right_image']:
        data = landing_page(
                    order = last_order+1,
                    h1 = 'lorem ipsum',
                    h2 = '',
                    p = 'lorem ipsum',
                    img = 'lorem ipsum',
                    read_link = '',
                    yt_link = 'lorem ipsum',
                    file_link = 'lorem ipsum',
                    yt_title = 'lorem ipsum',
                    file_title = 'lorem ipsum',
                    layout = layout_type,
                    background_color = '#ffff',
                    show_status = False,
        )
        data.save()
        return True

    elif layout_type in ['two_images']:
        data = landing_page(
                    order = last_order+1,
                    h1 = 'lorem ipsum',
                    h2 = 'lorem ipsum',
                    p = 'lorem ipsum',
                    img = 'lorem ipsum|lorem ipsum',
                    read_link = '',
                    yt_link = '',
                    file_link = '',
                    yt_title = '',
                    file_title = '',
                    layout = layout_type,
                    background_color = '#ffff',
                    show_status = False,
        )
        data.save()
        return True
    else:
        return False


def addTab(id,type1,array):
    arr = array
    arr.append({
            'data':'',
            'type':type1,
            'id':'bf'+str(id),
           })
    return arr