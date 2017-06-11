#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2017 GENEOS"
__license__ = "GPL 3.0"
__version__ = "1.00"

AYUDA="""
odoo_api.py - interface API para consumir los web service de odoo 8
-----------------------------------------------------------------------------------
Opciones: 
  --ayuda: este mensaje
  --debug: modo depuración (detalla y confirma las operaciones)
  
  --autentificar: se loguea en el servidor
    --version: version del servidor odoo
    --permiso: comprobar si tiene permiso para aceder a un modelo
    --buscar: muestra todos los registros de un modelo que cumplan con el filtro
    --campos: visualiza todos los campos de un modelo
    --listar: lista todos los registros de un modelo con un limite de filas


ejemplo:
python odoo_api.py --autentificar --listar
"""

import os, sys
import xmlrpclib

url = 'http://45.79.148.145:8069'


if __name__ == '__main__':
    if '--ayuda' in sys.argv:
        print AYUDA

    DEBUG = '--debug' in sys.argv
    
    try:
        if '--autentificar' in sys.argv:
            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

            db = 'demo'
            username = 'chasqui'
            password = 'test'
            uid = common.authenticate(db, username, password, {})

            if DEBUG:
                print 'id de la empresa'
                print uid
                print '--------------------'

            
            if '--version' in sys.argv:
                print 'version del servidor'
                print common.version()
                print '--------------------'


            if '--permiso' in sys.argv:
                result = models.execute_kw(db, uid, password,
                            'res.partner', 'check_access_rights',
                            ['read'], {'raise_exception': False})
                if result:
                    print 'permiso para aceder al modelo'
                else:
                    print 'no tiene permiso para aceder al modelo'

            if '--buscar' in sys.argv:
                #buscar en modelo res.partner
                result = models.execute_kw(db, uid, password,
                    'res.partner', 'search',
                    [[['customer', '=', True]]])
                
                print 'Muestra todos los IDs', result
                print '--------------------'

                if len(result)>0:
                    print 'tomamos el primer id y consultamos algunos campos ...'
                    ids = result[0]
                    lectura = models.execute_kw(db, uid, password,
                        'res.partner', 'read',
                        [ids], {'fields': ['name', 'country_id', 'comment']})
                    
                    print 'ID:', lectura['id']
                    print 'Name:', lectura['name']
                    print 'Comentario:', lectura['comment']
                    print 'Pais:', lectura['country_id']
                    print '--------------------'

            if '--campos' in sys.argv:
                #visualizar todos los campos del modelo
                print 'visualizar todos los campos del modelo'
                response = models.execute_kw(db, uid, password, 'res.partner', 
                            'fields_get', [], {'attributes': ['string', 'help', 'type']})

                print response
                print '--------------------'

            
            if '--listar' in sys.argv:
                #buscar y mostrar datos en una sola consulta
                print "filtrar todos los clientes y mostrarlos con un limite 10"
                cust = models.execute_kw(db, uid, password,
                    'res.partner', 'search_read',
                    [[['customer', '=', True]]],
                    {'fields': ['name', 'country_id', 'comment'], 'limit': 10})

                for item in cust:
                    print 'ID:', item['id']
                    print 'Name:', item['name']
                    print 'Comentario:', item['comment']
                    print 'Pais:', item['country_id']
                    print '--------------------'


    except Exception as e:
        raise e
    else:
        pass
