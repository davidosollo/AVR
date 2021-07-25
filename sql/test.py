#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 15:26:10 2020

@author: davidosollo
"""

"""
Created on Sun Nov 15 15:26:10 2020

@author: davidosollo
"""

ALLOWED_EXTENSIONS = {'cvs', 'xlsx',  'xlsm',  'xlsb', 'xltx'}

def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return 1
    else:
        return 0

           
a=allowed_file("david.cvs")
print("file=",a)