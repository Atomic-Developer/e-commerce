from flask import Blueprint,render_template,request,url_for, redirect,jsonify, session, current_app
from database.models.cliente import Cliente, Produtos
import hashlib
import os
import uuid







cliente_route = Blueprint('cliente', __name__)


"""
home - rota'/'
sobre_nos - rota '/sobre'
produtos - rota '/prod' 
criar_conta- '/criar_conta' 
login_usuario-'/login'
cliente_perfil-'/user_perfil'( id_usuario )
subir_produto -'/criar_produto'


"""

def config_hash_password(txt):
    hash_obj=hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

@cliente_route.route('/')
def config():

        return render_template('config.html')



@cliente_route.route('/home')
def home():
    return render_template('home.html')



@cliente_route.route('/sobre')
def sobre_nos():
    return render_template('sobre_nos.html')


@cliente_route.route('/prod')
def pag_produto():
    produtos = Produtos.select()
    return render_template('pag_produto.html',  produtos=produtos)


@cliente_route.route('/criar_conta', methods=['POST', 'GET'])
def cont_create():
    if request.method == 'POST':
        data = request.get_json()

        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')

        rua = data.get('rua')
        cep = data.get('cep')
        cidade = data.get('cidade')
        n_casa = data.get('n_casa')  
        bairro  = data.get('bairro')

        if Cliente.select().where(Cliente.email == email).exists():
            return {"error": "Email já cadastrado"}, 400

        Cliente.create(
            nome=nome,
            email=email,
            senha=config_hash_password(senha),
            rua=rua,
            cep=cep,
            cidade=cidade,
            n_casa=n_casa,
            bairro=bairro  
        )
        return {"success": True}, 200

    return render_template('criar_conta.html')







@cliente_route.route('/login', methods=['POST', 'GET'])
def login_usuario():
    if request.method == 'POST':
        login_data = request.get_json()

        email = login_data.get('email')
        senha = login_data.get('senha')

        admin_email = 'adm@123'
        admin_senha = '123adm'

        senha_hash = config_hash_password(senha)


        if email == admin_email and senha == admin_senha:
            session['admin'] = True
            return jsonify({"nome": "Admin"}), 200
        


        elif Cliente.select().where((Cliente.email == email) & (Cliente.senha == senha_hash)).exists():
            cliente = Cliente.get((Cliente.email == email) & (Cliente.senha == senha_hash))
            session['email_cliente'] = cliente.email
            session['nome_cliente'] = cliente.nome
            session['id_cliente'] = cliente.id
            session['rua_cliente'] = cliente.rua
            session['cep_cliente'] = cliente.cep
            session['cidade_cliente'] = cliente.cidade
            session['n_casa_cliente'] = cliente.n_casa
            session['bairro_cliente'] = cliente.bairro

            return jsonify({"nome": cliente.nome}), 200


        else:
            return jsonify(error="Email ou senha inválidos"), 401

    return render_template('login.html')


@cliente_route.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('cliente.login_usuario'))



@cliente_route.route('/perfil')
def perfil():
    if 'id_cliente' in session:
        return render_template('perfil_cliente.html',
                                nome=session['nome_cliente'], 
                                email= session['email_cliente'],
                                cep = session['cep_cliente'],
                                rua = session['rua_cliente'],
                                cidade = session['cidade_cliente'],
                                numero_da_casa= session['n_casa_cliente'],
                                bairro=session['bairro_cliente']
                                  )
    
    else:
        return render_template('login.html')
    


@cliente_route.route('/cliente/delete', methods=['DELETE'])
def delete_cliente():
    cliente_id = session['id_cliente']
    cliente = Cliente.get(Cliente.id == cliente_id)


    if cliente:
        cliente.delete_instance()
        session.clear()
        return ''
    


@cliente_route.route('/criar_produto', methods=['POST', 'GET'])
def subir_produto():
    if session.get('admin') == True:
        if request.method == 'POST':
            categoria = request.form['categoria']
            nome = request.form['nome']
            marca = request.form['marca']
            desc=request.form['desc']
            preco = request.form['preco']

            imagem = request.files['foto']

            UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'imagem_produtos')
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Pega a extensão original da imagem
            ext = os.path.splitext(imagem.filename)[1]

            # Gera um nome único
            novo_nome = f"{uuid.uuid4().hex}{ext}"
            
            caminho_arquivo = os.path.join(UPLOAD_FOLDER, novo_nome)
            imagem.save(caminho_arquivo)

            caminho_relativo = os.path.join('imagem_produtos', novo_nome).replace('\\', '/')


            Produtos.create(
                categoria=categoria,
                nome=nome,
                marca=marca,
                desc=desc,
                preco_unitario=preco,
                foto=caminho_relativo
            )

            return render_template('upload_prod.html')
        else:
            return render_template('upload_prod.html')
    else:
        return redirect('/login')
    
@cliente_route.route('/lista_prod_admin')
def listage_produtos():
    produtos = Produtos
    return render_template('lista_de_produtos.html', produtos=produtos)



@cliente_route.route('/produto/<int:id_produto>')
def produto(id_produto):
    try:
        produto = Produtos.get(Produtos.id == id_produto)
        return render_template('produto_detalhe.html', produto=produto)
    except Produtos.DoesNotExist:
        return "Produto não encontrado", 404

@cliente_route.route('/buy/<int:id_produto>')
def buyProduto(id_produto):
    # testa se o user tá logado
    if 'id_cliente' not in session:
        return redirect(url_for('cliente.login_usuario'))

    try:
        produto = Produtos.get(Produtos.id == id_produto)
        return render_template('compra_page.html', produto=produto)
    except Produtos.DoesNotExist:
        return "Produto não encontrado", 404