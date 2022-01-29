# how to use
#
# fsm = Qu_fsm("path.json")
#
# fsm.set_default_attrs(attr1 = "value", attr2 = "value", ...)
# more important -> less important attributes
# WARNING while reconfigure default attrs, delete (edit) path.json
#
# @fsm.method(attrn = "value", ...)
# @fsm.method(attrn = "value2", ...)
# def foo(*args):
#   pass
#
# @fsm.methods(attrn = "value", attrm = ["v1", "v2"], ...)
# def bar(*args):
#   pass
#
# fsm.change_attrs(**attrs)
# to change _current_attrs
#
# handle_command(*args)
# call the function by _current_attrs

from qu_json import*
from itertools import product

class Qu_fsm:
    _all_methods = dict()
    _all_attrs = dict()
    _wrapped_all_attrs = dict()
    _current_attrs = dict()

    def __init__(self, file_path):
        self._json_file = Qu_json(file_path)

    def set_default_attrs(self, **attrs):
        if self._all_methods:
            raise Exception("You can set attrs only before functions definition")
        for key in attrs:
            self._all_attrs[key] = attrs[key]
            self._wrapped_all_attrs[key] = [attrs[key]]

        if self._json_file.data:    # if data exists  
            if self._json_file.data.keys() != attrs.keys():
                raise Exception("Reconfigured default attrs, firstly delete " + self._json_file.file_path)

            self._current_attrs = self._json_file.data
        else:
            self._current_attrs = dict(self._all_attrs)
            self._json_file.data = self._current_attrs
            self._json_file.save()

    def get_attr(self, attr_name):
        return self._current_attrs[attr_name]

    def change_attrs(self, **attrs):
        for key in attrs:
            if key not in self._current_attrs:
                raise NameError
            else:
                self._current_attrs[key] = attrs[key]
                
        self._json_file.save()
                
    def method(self, **attrs):  
        def wrap(func):
            out_attrs = dict(self._all_attrs) 
            
            for key in attrs:
                out_attrs[key] = attrs[key]
                
            self._all_methods[str(out_attrs)] = func
            return func
        return wrap

    def methods(self, **raw_attrs):  
        def wrap(func):
            # wrapping single attrs to list
            attrs = { key : raw_attrs[key] if type(raw_attrs[key]) == list else [raw_attrs[key]] for key in raw_attrs }      
            pre_out_attrs = dict(self._wrapped_all_attrs)
            
            for key in attrs:
                pre_out_attrs[key] = attrs[key]

            for out_attrs_set in product(*pre_out_attrs.values()):
                out_attrs = dict()
                key_order = 0
                
                for key in self._all_attrs:
                    out_attrs[key] = out_attrs_set[key_order]
                    key_order += 1
                
                self._all_methods[str(out_attrs)] = func
                
            return func
        return wrap

    def handle_method(self, *args, strict = False):   
        out_attrs = dict(self._current_attrs)
        keys = list(self._current_attrs)[::-1]

        if str(out_attrs) in self._all_methods:
            self._all_methods[str(out_attrs)](*args)
            return True

        if strict: return False
        
        for key in keys:
            out_attrs[key] = self._all_attrs[key]
            if str(out_attrs) in self._all_methods:
                self._all_methods[str(out_attrs)](*args)
                return True

        return False

    # returns the function by current state (+attrs) or None
    def get_method(self, strict = False, **attrs):
        out_attrs = dict(self._current_attrs)
        
        for key in attrs:
            out_attrs[key] = attrs[key]

        if str(out_attrs) in self._all_methods:
            return self._all_methods[str(out_attrs)]
            
        if strict: return None

        keys = list(self._current_attrs)[::-1]
        
        for key in keys:
            out_attrs[key] = self._all_attrs[key]
            if str(out_attrs) in self._all_methods:
                return self._all_methods[str(out_attrs)]

        return None

    # returns the function by attrs or None
    def find_method(self, **attrs):
        out_attrs = dict(attrs)
        keys = list(attrs)[::-1]

        for key in self._all_attrs:
            if key not in attrs:
                out_attrs[key] = self._all_attrs[key]

        if str(out_attrs) in self._all_methods:
            return self._all_methods[str(out_attrs)]
            
        return None 

