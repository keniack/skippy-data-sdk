import logging

from kubernetes import config, watch, client
from kubernetes.client import V1Pod
from minio import Minio
from minio.error import ResponseError



def consume(urn):
    def wrapper(func):
        logging.info('Consume.wrapper(%s)'% func)
        def call(*args, **kwargs):
            logging.info('Consume.call(%s,%s,%s)'% (func,args,kwargs))
            post_data = json.dumps(s3_config['consume'])
            logging.info('POST Data(%s)' % post_data)
            response = requests.get(url=url,headers={'content-type':'application/json'},data=post_data)
            logging.info('Response (%s)'% response)
            if response.status_code!=200:
                sys.exit("Error calling wrapper, expected: %d, got: %d\n" % (200, response.status_code))
            logging.info('Response Data(%s)' % response.text)
            kwargs['data'] = response.text
            return func(*args, **kwargs)
        logging.debug('Consume.wrapper over')
        return call
    return wrapper