from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date



# Create your models here.
STATUS_CHOICES = [
    ('Pendente', 'Pendente'),
    ('Em produção', 'Em produção'),
    ('Finalizado', 'Finalizado'),
    ('Cancelado', 'Cancelado'),
]

TIPO_CHOICES = [
    ('Ingrediente', 'Ingrediente'),
    ('ProdutoAcabado', 'ProdutoAcabado'),
]


class Funcionario(models.Model):
    nome_funcionario = models.CharField(max_length=100)
    tipo_funcionario = models.CharField(max_length=100)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nome_funcionario

class GrupoCategoria(models.Model):
    nome_grupo_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_grupo_categoria

class SubgrupoSubcategoria(models.Model):
    nome_subgrupo_subcategoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_subgrupo_subcategoria
    
class Marca(models.Model):
    nome_marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_marca

class Fabricante(models.Model):
    razao_social = models.CharField(max_length=100)

    def __str__(self):
        return self.razao_social 
    
class Tipo(models.Model):
    nome_tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_tipo

class UnidadeMedida(models.Model):
    nome_unidade_medida = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome_unidade_medida
    
class TipoEmbalagem(models.Model):
    nome_tipo_embalagem = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_tipo_embalagem

class AtividadeServico(models.Model):
    atividade_servico = models.CharField(max_length=100)

    def __str__(self):
        return self.atividade_servico


class MateriaPrima(models.Model):
    nome_materia_prima = models.CharField(max_length=100)
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoCategoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES, default='Ingrediente')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.nome_materia_prima

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE)
    grupo = models.ForeignKey(GrupoCategoria, on_delete=models.CASCADE)
    subgrupo = models.ForeignKey(SubgrupoSubcategoria, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES, default='ProdutoAcabado')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    estoque_minimo = models.IntegerField(default=0)
    estoque_maximo = models.IntegerField(default=0)
    preco_produto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lucro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.pk:
            produto_antigo = Produto.objects.get(pk=self.pk)
            if self.preco_produto != produto_antigo.preco_produto:
                HistoricoPreco.objects.create(
                    produto=produto_antigo,
                    preco_anterior=produto_antigo.preco_produto,
                    preco_atual=self.preco_produto,  # Adicionando o preço atual
                    origem=HistoricoPreco.PRODUTO
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_produto
    
class HistoricoPreco(models.Model):
    ENTRADA = 'E'
    SAIDA = 'S'
    PRODUTO = 'P'
    ORIGEM_CHOICES = [
        (ENTRADA, 'Entrada de Produtos'),
        (SAIDA, 'Saída de Produtos'),
        (PRODUTO, 'Produto'),
    ]

    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    preco_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    preco_atual = models.DecimalField(max_digits=10, decimal_places=2)
    data_modificacao = models.DateTimeField(default=timezone.now)
    origem = models.CharField(max_length=1, choices=ORIGEM_CHOICES)

    def __str__(self):
        return f'{self.produto} - De: {self.preco_anterior}R$ para: {self.preco_atual}R$ - Origem: {self.get_origem_display()}'

class CustoGeral(models.Model):
    numero_de_itens = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    custo_indireto_por_unidade = models.IntegerField(verbose_name='Custo Indireto por Unidade(Rateio)', blank=True, null=True)
    custo_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    receita = models.ForeignKey('Receita', on_delete=models.CASCADE, related_name='custo_geral')
    data_inicio = models.DateField(verbose_name='Data Início', blank=True, null=True)
    data_fim = models.DateField(verbose_name='Data Fim', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Realiza o cálculo dos custos sempre que o objeto for salvo
        calcular_custos(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Número de Itens Produzidos : {self.numero_de_itens} - Custo Indireto por Unidade(Rateio): {self.custo_indireto_por_unidade}'


class CentroDeCusto(models.Model):
    tipo_despesa = models.CharField(max_length=100)
    rateio = models.BooleanField(default=False)

    def __str__(self):
        return self.tipo_despesa


class SubCentroDeCusto(models.Model):
    sub_custos_totais = models.ForeignKey(CustoGeral, on_delete=models.CASCADE, related_name='custos_set')
    tipo_despesa = models.ForeignKey(CentroDeCusto, on_delete=models.CASCADE)
    nome_despesa = models.CharField(max_length=100)
    valor_despesa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.tipo_despesa.tipo_despesa} - {self.nome_despesa} - {self.valor_despesa}'


class Receita(models.Model):
    nome_receita = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='receita_do_produto')
    informações_adicionais = models.TextField()
    custo_receita = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True, verbose_name='Custo da Receita')

    def atualizar_custo_receita(self):
        custo_total = (
            sum(ingrediente.valor_total for ingrediente in self.ingredientes_set.all()) +
            sum(execution.valor_da_execucao for execution in self.execucao_mao_de_obra_set.all() if execution.valor_da_execucao is not None) +
            sum(embalagem.valor_total for embalagem in self.embalagens_set.all()) +
            sum(imposto.valor_imposto for imposto in self.impostos_set.all()) if self.impostos_set.exists() else 0
        )
        self.custo_receita = custo_total
        self.save()

    def __str__(self):
        return self.nome_receita.nome_produto


class Ingredientes(models.Model):
    receita = models.ForeignKey(Receita, related_name='ingredientes_set', on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, limit_choices_to={'tipo': 'Ingrediente'})
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.materia_prima.valor_unitario  # Calcula o valor total
        super().save(*args, **kwargs)
        self.receita.atualizar_custo_receita()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.receita.atualizar_custo_receita()

    def __str__(self):
        return self.materia_prima.nome_materia_prima


class Embalagens(models.Model):
    receita = models.ForeignKey(Receita, related_name='embalagens_set', on_delete=models.CASCADE)
    embalagem = models.CharField(max_length=100)
    nome_tipo_embalagem = models.ForeignKey(TipoEmbalagem, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_embalagem = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_embalagem  # Calcula o valor total
        super().save(*args, **kwargs)
        self.receita.atualizar_custo_receita()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.receita.atualizar_custo_receita()

    def __str__(self):
        return self.embalagem


class ProducaoFuncionario(models.Model):
    receita = models.ForeignKey(Receita, related_name='execucao_mao_de_obra_set', on_delete=models.CASCADE)
    etapa_producao = models.ForeignKey(AtividadeServico, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    tempo_gasto = models.DecimalField(max_digits=10, decimal_places=2)
    valor_da_execucao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.valor_da_execucao = self.tempo_gasto * self.funcionario.valor_hora
        super().save(*args, **kwargs)
        self.receita.atualizar_custo_receita()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.receita.atualizar_custo_receita()


class Impostos(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='impostos_set')
    nome_imposto = models.CharField(max_length=100)
    valor_imposto = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.receita.atualizar_custo_receita()

    def __str__(self):
        return f'Nome do imposto: {self.nome_imposto} - Valor do imposto: {self.valor_imposto}'




class CustoGeralReadOnly(CustoGeral):
    class Meta:
        proxy = True
        verbose_name = 'Visualização de Custo Geral'
        verbose_name_plural = 'Visualizações de Custos Gerais'
    
class OrdemProducao(models.Model):
    funcionario_emitiu_ordem = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pendente')
    data_producao = models.DateField(verbose_name='Data de Produção', blank=True, null=True)  # Novo campo de data


    def __str__(self):
        return f'{self.funcionario_emitiu_ordem.nome_funcionario} - {self.status}'

class OrdemProducaoProduto(models.Model):
    ordem_producao_produto = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    quantidade_solicitada = models.IntegerField()
    quantidade_real_produzida = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return str(self.receita.nome_receita)


# Sinal para calcular custos após salvar um SubCentroDeCusto
@receiver(post_save, sender=SubCentroDeCusto)
def atualizar_custos(sender, instance, **kwargs):
    custo_geral = instance.sub_custos_totais
    calcular_custos(custo_geral)
    custo_geral.save()


# Função para calcular os custos em CustoGeral
def calcular_custos(custo_geral):
    if not custo_geral.pk:
        return  # Ensure the instance has a primary key

    # Verifica se as datas de início e fim foram fornecidas
    if custo_geral.data_inicio and custo_geral.data_fim:
        ordens_producao = OrdemProducaoProduto.objects.filter(
            receita=custo_geral.receita,
            ordem_producao_produto__data_producao__range=(custo_geral.data_inicio, custo_geral.data_fim)
        )
    else:
        ordens_producao = OrdemProducaoProduto.objects.filter(receita=custo_geral.receita)

    # Calcula a soma de todos os valores do campo quantidade_real_produzida das Ordens de Produção filtradas
    total_quantidade_produzida = ordens_producao.aggregate(Sum('quantidade_real_produzida'))['quantidade_real_produzida__sum'] or 0
    
    # Atualiza o campo numero_de_itens com a soma calculada
    custo_geral.numero_de_itens = total_quantidade_produzida
    
    if custo_geral.numero_de_itens > 0:
        custo_indireto_por_unidade = sum(sub_custo.valor_despesa for sub_custo in custo_geral.custos_set.all()) / custo_geral.numero_de_itens
        custo_geral.custo_indireto_por_unidade = custo_indireto_por_unidade
        custo_final = custo_indireto_por_unidade + custo_geral.receita.custo_receita
        custo_geral.custo_final = custo_final

    

class Destinatario(models.Model):
    destino_produto = models.CharField(max_length=100)

    def __str__(self):
        return self.destino_produto

class Setor(models.Model):
    setor = models.CharField(max_length=100)

    def __str__(self):
        return self.setor

class EntradaProduto(models.Model):
    data_hora = models.DateTimeField()
    fornecedor = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    num_nota_entrada = models.CharField(max_length=100)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Numero da nota: {self.num_nota_entrada} - Fornecedor: {self.fornecedor.razao_social}'

class EntradaProdutoItem(models.Model):
    entrada = models.ForeignKey(EntradaProduto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="produto_entrada_produto_item")
    quantidade = models.IntegerField()
    preco_entrada = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.produto.nome_produto
    
class SaidaProduto(models.Model):
    data_hora = models.DateTimeField()
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    num_nota_saida = models.CharField(max_length=100)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return f'Numero da nota: {self.num_nota_saida} - Destinatario: {self.destinatario.destino_produto}'

class SaidaProdutoItem(models.Model):
    saida = models.ForeignKey(SaidaProduto, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_saida = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.produto.nome_produto
    
class TesteQualidade(models.Model):
    teste_qualidade = models.CharField(max_length=100)

    def __str__(self):
        return self.teste_qualidade

class TesteQualidadeItem(models.Model):
    teste_qualidade = models.ForeignKey(TesteQualidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.teste_qualidade.teste_qualidade
