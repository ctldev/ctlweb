from .log import Log


def push(url, components=None, component_logs=None):
    """ Lists of components and component_logs are push to the ctlweb-frontend
    url. """
    import requests
    Log.debug('push() Uploading to url %s' % url)

    files = {}
    data = {}

    if components:
        comp = components.pop()
        manifest_file = comp._component_file
        files['manifest'] = open(manifest_file, 'rb')
    if component_logs:
        complog = component_logs.pop()
        data['exe_hash'] = complog.exe_hash
    if files or data:
        r = requests.post(url, data=data, files=files)
        if r.status_code != requests.codes.ok:
            Log.critical('Error %s occured while upload' % r.status_code)
    if components or component_logs:
        push(url, components, component_logs)
