from .log import Log


def push(url, components=None, component_logs=None):
    """ Lists of components and component_logs are push to the ctlweb-frontend
    url. """
    import requests
    Log.debug('push() Uploading to url %s' % url)

    files = {}
    data = {}
    info_data = {'manifest': 'no manifest',
                 'hash': 'no hash'}

    if components:
        comp = components.pop()
        manifest_file = comp._component_file
        files['manifest'] = open(manifest_file, 'rb')
        info_data['manifest'] = manifest_file
    if component_logs:
        complog = component_logs.pop()
        data['exe_hash'] = complog.hash
        info_data['hash'] = complog.hash
    if files or data:
        Log.info('Uploading {hash} and {manifest}'.format(**info_data))
        r = requests.post(url, data=data, files=files)
        if r.status_code != requests.codes.ok:
            Log.warning('Error %s occured while upload' % r.status_code)
    if components or component_logs:
        push(url, components, component_logs)
