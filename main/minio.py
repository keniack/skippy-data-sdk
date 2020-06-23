import os
import logging


from kubernetes import config, watch, client
from kubernetes.client import V1Pod
from minio import Minio
from minio.error import ResponseError


def find_minio_pods(bucket: str, file_name: str) -> None:
    logging.debug('resolve minio pods...')
    api = client.CoreV1Api()
    # field selectors are a string, you need to parse the fields from the pods here
    app = 'minio'
    ret = api.list_pod_for_all_namespaces(watch=False, label_selector="app=" + app)
    for i in ret.items:
        for c in filter(lambda co: co.name == app, i.spec.containers):
            for p in c.ports:
                logging.info('ip: %s, port: %s' % (i.status.pod_ip, p.container_port))
                logging.info(
                    'pod_has_file: %s' % has_pod_file(bucket, file_name, str(i.status.pod_ip), str(p.container_port)))
                list_objects_minio(i.status.pod_ip, p.container_port,bucket)
                list_objects_minio(i.status.pod_ip, p.container_port)


def is_storage_pod(pod: V1Pod) -> bool:
    logging.debug('resolve minio pods...')
    # field selectors are a string, you need to parse the fields from the pods here
    app = 'minio'
    return any(filter(lambda co: co.name == app, pod.spec.containers))


def list_objects_minio(ip: str, port: str, bucket=None) -> None:
    try:
        client = minio_client(ip, port)
        if not bucket:
            buckets = minio_client(ip, port).list_buckets()
            for b in buckets:
                logging.info('List files in bucket  : %s' % b.name)
                objects = client.list_objects(b.name, recursive=True)
                for obj in objects:
                    logging.info('File Name: %s, Size: %s'%(obj.object_name.encode('utf-8'), obj.size))
        else:
            logging.info('List files in bucket  : %s'% bucket)
            objects = client.list_objects(str(bucket), recursive=True)
            for obj in objects:
                logging.info('File Name: %s, Size: %s'%(obj.object_name.encode('utf-8'), obj.size))
    except ResponseError as err:
        logging.exception('MinioClientException: %s', err)


def has_pod_file(bucket: str, file_name: str, ip: str, port: str) -> bool:
    try:
        stat = minio_client(ip, port).stat_object(bucket, file_name)
        return stat.size > 0
    except ResponseError as err:
        logging.exception('MinioClientException: %s', err.message)


def minio_client(ip: str, port: str) -> Minio:
    minio_ac = os.environ.get('MINIO_AC', None)
    minio_sc = os.environ.get('MINIO_SC', None)
    logging.debug('Minio ACCESS_KEY: %s'% minio_ac)
    logging.debug('Minio SECRET_KEY: %s'% minio_sc)
    minio_addr = ('%s:%s'%(ip, port))
    logging.debug('Connecting to pod : %s'% minio_addr)
    client = Minio(minio_addr,
                   access_key=minio_ac,
                   secret_key=minio_sc,
                   secure=False)
    return client
