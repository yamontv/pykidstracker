"""This module serves the WEB"""
from configparser import ConfigParser
from bottle import route, run, static_file, request

config = ConfigParser(allow_no_value=True)
config.read('config.ini')


@route('/content/map')
def map_content():
    return '<h1>Map</h1>'


@route('/content/chat')
def chat_content():
    return '<h1>Chat</h1>'


@route('/content/hearts')
def hearts_content():
    return '<h1>Hearts</h1>'


@route('/submit/config', method='POST')
def do_login():
    config['contact1']['name'] = request.forms.get('contact1_name')
    config['contact1']['phone'] = request.forms.get('contact1_num')
    config['contact2']['name'] = request.forms.get('contact2_name')
    config['contact2']['phone'] = request.forms.get('contact2_num')
    config['contact3']['name'] = request.forms.get('contact3_name')
    config['contact3']['phone'] = request.forms.get('contact3_num')
    config['main']['interval'] = request.forms.get('interval')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return '{"command": 1}'


@route('/content/config')
def config_content():
    def contact_field(caption, idx, name, number):
        html = '<div class="form-group row">'
        html += '<label for="contact" class="col-sm-2 col-form-label">{}</label>'.format(
            caption)
        html += '<div class="col-sm-5">'
        html += '<input type="text" class="form-control" placeholder="Name"'
        html += 'id="{}_name" name="{}_name" value="{}">'.format(
            idx, idx, name if name else '')
        html += '</div>'
        html += '<div class="col-sm-5">'
        html += '<input type="text" class="form-control" placeholder="Phone Number"'
        html += 'id="{}_num" name="{}_num" value="{}">'.format(
            idx, idx, number if number else '')
        html += '</div>'
        html += '</div>'
        return html

    def text_field(caption, idx, holder, value):
        html = '<div class="form-group row">'
        html += '<label for="interval" class="col-sm-2 col-form-label">{}</label>'.format(
            caption)
        html += '<div class="col-sm-10">'
        html += '<input type="text" class="form-control" placeholder="{}"'.format(
            holder)
        html += 'id="{}" name="{}" value="{}">'.format(idx, idx,
                                                       value if value else '')
        html += '</div>'
        html += '</div>'
        return html

    html = '<form id="config_form" role="form">'
    html += contact_field('Contact 1', 'contact1', config['contact1']['name'],
                          config['contact1']['phone'])
    html += contact_field('Contact 2', 'contact2', config['contact2']['name'],
                          config['contact2']['phone'])
    html += contact_field('Contact 3', 'contact3', config['contact3']['name'],
                          config['contact3']['phone'])
    html += text_field('Update Interval', 'interval', 'Seconds',
                       config['main']['interval'])
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


run(host='0.0.0.0', port=int(config['main']['http_port']))
