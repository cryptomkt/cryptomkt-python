
from operator import itemgetter
import diff_match_patch as dmp_module

import json

dmp = dmp_module.diff_match_patch()

def is_value(value):
    return isinstance(value, list)

def is_object(value):
    return isinstance(value, dict) and not '_t' in value.keys()

def is_string(value):
    return isinstance(value, str) 

def is_array(value):
    return isinstance(value, dict) and '_t' in value.keys()

def is_removal(value):
    return len(value) == 3 and value[2] == 0

def is_text_modification(value):
    return len(value) == 3 and value[2] == 2

def is_movement(value):
    return len(value) == 3 and value[2] == 3

def is_addition(value):
    return len(value) == 1

def is_modification(value):
    return len(value) == 2


def is_old_index(key):
    return len(key) >= 2 and key[0] == '_' and key[1] != 't'

def is_new_index(key):
    return len(key) > 0 and key[0] != '_'


def patch(dict_, delta):
    if is_object(delta):
        patch_object(dict_, delta)
    elif is_array(delta):
        patch_array(dict_, delta)
    elif is_string(delta):
        patch(dict_, json.loads(delta))

def patch_object(dict_, delta):
    for key, v in delta.items():
        # if the change is over a value
        if is_value(v):
            if is_addition(v):
                dict_.update({key:v[0]})
            elif is_modification(v):
                dict_.update({key:v[1]})
            elif is_text_modification(v):
                patches = dmp.patch_fromText(v[0])
                new_text = dmp.patch_apply(patches, dict_[key])[0]
                dict_.update({key:new_text})
            elif is_removal(v):
                del dict_[key]

        # if the change is inside an inner object.
        else:
            patch(dict_[key], v)                

def patch_array(arr, delta):
    # first we remove and store moves values, then we add, pushing the tail if necessary.
    # so, first are procesed the '_n', then are procesed 'n'
    to_remove = list()
    to_add = list()
    for key, v in delta.items():
        if is_old_index(key):
            idx = int(key[1:])
            # the only possibilities are a removal and a movement, in both
            # cases the old value is removed, and in the movement case,
            # the old value is aldo added to the new array, in the new index
            to_remove.append(idx)

            #if is_removal(value): pass
            if is_value(v) and is_movement(v):
                to_add.append((v[1], arr[idx]))

        elif is_new_index(key):
            idx = int(key)

            if is_value(v) and is_addition(v):
                to_add.append((idx, v[0]))
    
    
    # recursion is first, then elimination and finally adition.
    # at this point, recursion is already finished. so we proced with removal, then adition
    # sort in descending order, by index
    to_remove.sort(reverse=True)
    for idx in to_remove:
        del arr[idx]
    
    # append the new elements
    # sort in ascending order, by their new index
    to_add.sort(key=itemgetter(0))
    for (idx, val) in to_add:
        arr.insert(idx, val)
    
    for key, v in delta.items():
        if is_new_index(key):
            idx = int(key)
            patch(arr[idx], v)

        

    