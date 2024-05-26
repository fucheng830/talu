import imp    
    
def import_from_string(content, module_name, file_name=None):
    if not file_name:
        file_name = '{0}.py'.format(module_name)
        
    value = compile(content, file_name, 'exec')
    module = imp.new_module(module_name)
    exec (value, module.__dict__)
    return module

if __name__=='__main__':
    content = """
import datetime

def run():
    print(datetime.datetime.now())

if __name__=='__main__':
    run()
"""
    m = import_from_string(content, 'test')
    m.run()
