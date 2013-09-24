import Log


def push(url, components=None, component_logs=None):
    """ Lists of components and component_logs are push to the ctlweb-frontend
    url. """
    import requests
    Log.debug('push() Uploading to url %s' % url)

    content = {}

    if components:
        comp = components.pop()
        manifest_file = comp._component_file
        content['manifest'] = open(manifest_file, 'rb')
    if component_logs:
        complog = component_logs.pop()
        content['exe_hash'] = complog.exe_hash
    if content:
        r = requests.post(url, data=content)
        if r.status_code != requests.codes.ok:
            Log.critical('Error %s occured while upload' % r.status_code)
    if components or component_logs:
        push(url, components, component_logs)
