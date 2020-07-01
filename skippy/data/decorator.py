import logging

from skippy.data.minio import upload_file, download_files


def consume(urns):
    def wrapper(func):
        logging.info('Consume.wrapper(%s)' % func)

        def call(*args, **kwargs):
            logging.info('Consume.call(%s,%s,%s)' % (func, args, kwargs))
            artifact = download_files(urns)
            logging.info('Content Data(%s)' % artifact)
            kwargs['data'] = artifact
            return func(*args, **kwargs)

        logging.debug('Consume.wrapper over')
        return call

    return wrapper


def produce(urn):
    def wrapper(func):
        logging.info('Produce.wrapper(%s)' % func)

        def call(*args, **kwargs):
            logging.info('Produce.call(%s,%s,%s)' % (func, args, kwargs))
            response = func(*args, **kwargs)
            upload_file(urn, response)
            logging.info('Produce.store(%s)' % response)
            return response

        logging.debug('Produce.wrapper over')
        return call

    return wrapper


def findDecorators(target):
    import ast, inspect
    res = {}

    def visit_FunctionDef(node):
        res[node.name] = [ast.dump(e) for e in node.decorator_list]

    V = ast.NodeVisitor()
    V.visit_FunctionDef = visit_FunctionDef
    V.visit(compile(inspect.getsource(target), '?', 'exec', ast.PyCF_ONLY_AST))
    return res
