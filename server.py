from bottle import route, run, template, static_file


@route('/content/map')
def map_content():
    return '<h1>Map</h1>'


@route('/content/chat')
def chat_content():
    return '<h1>Chat</h1>'


@route('/content/hearts')
def hearts_content():
    return '<h1>Hearts</h1>'


@route('/content/config')
def config_content():
    def contact_field(caption, idx, name, number):
        html = '<div class="form-group row">'
        html += '<label for="contact" class="col-sm-2 col-form-label">{}</label>'.format(
            caption)
        html += '<div class="col-sm-5">'
        html += '<input type="email" class="form-control" placeholder="Name"'
        html += 'id="{}_name" value="{}">'.format(idx, name if name else '')
        html += '</div>'
        html += '<div class="col-sm-5">'
        html += '<input type="email" class="form-control" placeholder="Phone Number"'
        html += 'id="{}_num" value="{}">'.format(idx, number if number else '')
        html += '</div>'
        html += '</div>'
        return html

    def text_field(caption, idx, holder, value):
        html = '<div class="form-group row">'
        html += '<label for="interval" class="col-sm-2 col-form-label">{}</label>'.format(
            caption)
        html += '<div class="col-sm-10">'
        html += '<input type="email" class="form-control" placeholder="{}"'.format(
            holder)
        html += 'id="{}_name" value="{}">'.format(idx, value if value else '')
        html += '</div>'
        html += '</div>'
        return html

    html = '<form>'
    html += contact_field('Contact 1', 'contact1', None, None)
    html += contact_field('Contact 2', 'contact2', None, None)
    html += contact_field('Contact 3', 'contact2', None, None)
    html += text_field('Update Interval', 'interval', 'Seconds', None)
    html += '<button type="submit" class="btn btn-primary">Write Config</button>'
    html += '</form> '

    return html


@route('/content/spy')
def spy_content():
    return '<h1>Spy</h1>'


@route('/')
def home_route():
    return static_file("index.html", root='static')


@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


run(host='localhost', port=8080)
