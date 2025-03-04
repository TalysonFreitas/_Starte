from rolepermissions.roles import AbstractUserRole

class Artista(AbstractUserRole):
    available_permissions = {
        'cadastrar_produto': True,
        'ver_produto': True,
        'editar_produto': True,
        'excluir_produto': True
        
    }
    
class Comprador(AbstractUserRole):
    available_permissions = {
        'realizar_pedido': True
    }
    
