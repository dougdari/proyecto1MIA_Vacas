import ply.lex as lex
import ply.yacc as yacc


tokens = (
    'CONFIGURE',
    'CREATE',
    'DELETE',
    'COPY',
    'TRANSFER',
    'RENAME',
    'MODIFY',
    'ADD',
    'BACKUP',
    'EXEC',
    'LOCAL',
    'CLOUD',
    'TO',
    'DIRECTORIO_CON_ARCHIVO',
    'DIRECTORIO_CON_ARCHIVO_COMILLAS',
    'NOMBRE_ARCHIVO',
    'NOMBRE_ARCHIVO_COMILLAS',
    'SOLO_DIRECTORIO',
    'SOLO_DIRECTORIO_COMILLAS',
    'FROM',
    'MODE',
    'BODY',
    'PATH',
    'FALSE',
    'TRUE',
    'FLECHA',
    'SEPARADOR',
    'TYPE',
    'ENCRYPT_LOG',
    'ENCRYPT_READ',
    'LLAVE',
    'NAME',
    'CADENA',
)

t_CONFIGURE = r'(C|c)(O|o)(N|n)(F|f)(I|i)(G|g)(U|u)(R|r)(E|e)'
t_CREATE = r'(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)'
t_DELETE = r'(D|d)(E|e)(L|l)(E|e)(T|t)(E|e)' 
t_COPY = r'(C|c)(O|o)(P|p)(Y|y)'
t_TRANSFER = r'(T|t)(R|r)(A|a)(N|n)(S|s)(F|f)(E|e)(R|r)'
t_RENAME = r'(R|r)(E|e)(N|n)(A|a)(M|m)(E|e)'
t_MODIFY = r'(M|m)(O|o)(D|d)(I|i)(F|f)(Y|y)'
t_ADD = r'(A|a)(D|d)(D|d)'
t_BACKUP = r'(B|b)(A|a)(C|c)(K|k)(U|u)(P|p)'
t_EXEC = r'(E|e)(X|x)(E|e)(C|c)'
t_LOCAL = r'(L|l)(O|o)(C|c)(A|a)(L|l)'
t_CLOUD = r'(C|c)(L|l)(O|o)(U|u)(D|d)'

t_TO = r'to'
t_DIRECTORIO_CON_ARCHIVO = r'[\/]([a-zA-Z0-9_-]+[\/])*[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
t_DIRECTORIO_CON_ARCHIVO_COMILLAS = r'\"[\/]([a-zA-Z0-9_ -]+[\/])*[a-zA-Z0-9_ -]+\.[a-zA-Z0-9_-]+\"'

t_NOMBRE_ARCHIVO = r'[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
t_NOMBRE_ARCHIVO_COMILLAS = r'\"[a-zA-Z0-9 _-]+\.[a-zA-Z0-9_-]+\"'

t_SOLO_DIRECTORIO = r'[\/]([a-zA-Z0-9_-]+[\/])*'
t_SOLO_DIRECTORIO_COMILLAS = r'\"[\/]([a-zA-Z0-9 _-]+[\/])*\"'

t_FROM = r'from'
t_PATH = r'path'
t_BODY = r'body'
t_MODE = r'mode'
t_TRUE = r'true'
t_FALSE = r'false'
t_FLECHA = r'(-|–)>'
t_SEPARADOR = r'(-|–)'
t_TYPE = r'type'
t_ENCRYPT_LOG = r'encrypt_log'
t_ENCRYPT_READ = r'encrypt_read'
t_NAME = r'name'
t_LLAVE = r'llave'
t_CADENA = r'\"[^\"]*\"'

t_ignore = ' \t\n'

def t_error(t):
    print("Error lexico: {}".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

comandos = []

def p_inicio(p):
    '''
        inicio : l_comando
    '''

    print(comandos)

def p_l_comando(p):

    '''
    l_comando : l_comando comando
            | comando
    '''

    if len(p) > 2:
        comandos.append(p[2])
    else:
        comandos.append(p[1])

def p_comando(p): 
    '''
    comando : c_configure
           | c_create
           | c_delete
           | c_copy
           | c_transfer
           | c_rename
           | c_modify
           | c_add
           | backup
           | c_exec
    '''
    
    p[0] = p[1]

def p_c_exec(p):
    '''
        c_exec : EXEC SEPARADOR PATH FLECHA nt_directorio_con_archivo
    '''

    p[0] = ['exec', str(p[5])]

def p_c_add(p):
    '''
        c_add : ADD SEPARADOR PATH FLECHA nt_directorio_con_archivo SEPARADOR BODY FLECHA CADENA
    '''

    p[0] = ['add', str(p[5]), str(p[9])]

def p_c_modify(p):
    '''
        c_modify : MODIFY SEPARADOR PATH FLECHA nt_directorio_con_archivo SEPARADOR BODY FLECHA CADENA
    '''

    p[0] = ['modify', str(p[5]), str(p[9])]

def p_c_rename(p):
    '''
        c_rename : RENAME SEPARADOR PATH FLECHA nt_directorio_con_archivo SEPARADOR NAME FLECHA nt_nombre_archivo
    '''

    p[0] = ['rename', str(p[5]), str(p[9])]

def p_c_transfer(p):
    '''
        c_transfer : TRANSFER SEPARADOR FROM FLECHA nt_directorio_con_archivo SEPARADOR TO FLECHA nt_solo_directorio SEPARADOR MODE FLECHA tipo_modo 
    '''

    p[0]  = ['transfer', str(p[5]), str(p[9]), str(p[13])]

def p_c_copy(p):
    '''
        c_copy : COPY SEPARADOR FROM FLECHA nt_directorio_con_archivo SEPARADOR TO FLECHA nt_solo_directorio
    '''

    p[0] = ['copy',str(p[5]),str(p[9])]

def p_nt_directorio_con_archivo(p):
    '''
        nt_directorio_con_archivo : DIRECTORIO_CON_ARCHIVO
                                 | DIRECTORIO_CON_ARCHIVO_COMILLAS
                                 | nt_solo_directorio
    '''
    p[0] = str(p[1])

def p_c_delete(p):
    '''
        c_delete : DELETE SEPARADOR PATH FLECHA nt_solo_directorio SEPARADOR NAME FLECHA nt_nombre_archivo
                 | DELETE SEPARADOR PATH FLECHA nt_solo_directorio
    '''

    if len(p) > 6:
        p[0] = ['delete',str(p[5]),str(p[9])]
    else:
        p[0] = ['delete',str(p[5])]

def p_c_create(p):
    '''
        c_create : CREATE SEPARADOR NAME FLECHA nt_nombre_archivo SEPARADOR PATH FLECHA nt_solo_directorio SEPARADOR BODY FLECHA CADENA
    '''
    p[0] = ['create',str(p[5]),str(p[9]),str(p[13])]    

def p_nt_solo_directorio(p):
    '''
        nt_solo_directorio : SOLO_DIRECTORIO
                           | SOLO_DIRECTORIO_COMILLAS
    '''
    p[0] = str(p[1])

def p_nt_nombre_archivo(p):
    '''
        nt_nombre_archivo : NOMBRE_ARCHIVO
                          | NOMBRE_ARCHIVO_COMILLAS
    '''
    p[0] = str(p[1])

def p_c_configure(p):
    '''
      c_configure : CONFIGURE SEPARADOR TYPE FLECHA tipo_modo SEPARADOR ENCRYPT_LOG FLECHA booleanos SEPARADOR ENCRYPT_READ FLECHA booleanos SEPARADOR LLAVE FLECHA CADENA
                  | CONFIGURE SEPARADOR TYPE FLECHA tipo_modo SEPARADOR ENCRYPT_LOG FLECHA booleanos SEPARADOR ENCRYPT_READ FLECHA booleanos
    '''

    if len(p) > 14:
        p[0]=['configure',str(p[5]),str(p[9]),str(p[13]),str(p[17])]
        #print(p[0])
    else :
        p[0]=['configure',str(p[5]),str(p[9]),str(p[13])]
        #print(p[0])


def p_backup(p):
    '''
        backup : BACKUP
    '''
    p[0]=['backup']

def p_tipo_modo(p):
    '''
    tipo_modo : LOCAL
             | CLOUD
    '''

    p[0] = str(p[1])

def p_booleanos(p):
    '''
    booleanos : TRUE
             | FALSE
    '''
    p[0] = str(p[1])

def p_error(p):
    print("Error sintactico")


parser = yacc.yacc()
 
entrada = "exec -path->/home/Desktop/calificacion.mia modify -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\" add -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\""

resultado = parser.parse(entrada, lexer=lexer)

print("Resultado: {}".format(resultado))