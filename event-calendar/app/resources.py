from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import *

class IngredientesExportResource(resources.ModelResource):
    receita = fields.Field(
        column_name='receita',
        attribute='receita',
        widget=ForeignKeyWidget(Receita, 'nome_receita')
    )

    materia_prima = fields.Field(
        column_name='materia_prima',
        attribute='materia_prima__nome_materia_prima'
    )

    quantidade = fields.Field(
        column_name='quantidade',
        attribute='quantidade'
    )

    valor_total = fields.Field(
        column_name='valor_total',
        attribute='valor_total'
    )

    class Meta:
        model = Ingredientes
        export_order = ('id', 'receita', 'materia_prima', 'quantidade', 'valor_total')

class EmbalagensExportResource(resources.ModelResource):
    receita = fields.Field(
        column_name='receita',
        attribute='receita',
        widget=ForeignKeyWidget(Receita, 'nome_receita')
    )

    embalagem = fields.Field(
        column_name='embalagem',
        attribute='embalagem'
    )

    nome_tipo_embalagem = fields.Field(
        column_name='nome_tipo_embalagem',
        attribute='nome_tipo_embalagem__nome_tipo_embalagem'
    )

    quantidade = fields.Field(
        column_name='quantidade',
        attribute='quantidade'
    )

    valor_embalagem = fields.Field(
        column_name='valor_embalagem',
        attribute='valor_embalagem'
    )

    valor_total = fields.Field(
        column_name='valor_total',
        attribute='valor_total'
    )

    class Meta:
        model = Embalagens
        export_order = ('id', 'receita', 'embalagem', 'nome_tipo_embalagem', 'quantidade', 'valor_embalagem', 'valor_total')

class ReceitaExportResource(resources.ModelResource):
    ingredientes = fields.Field(
        column_name='ingredientes',
        attribute='ingredientes_set',
        widget=ForeignKeyWidget(Ingredientes, 'materia_prima__nome_materia_prima')
    )

    embalagens = fields.Field(
        column_name='embalagens',
        attribute='embalagens_set',
        widget=ForeignKeyWidget(Embalagens, 'embalagem')
    )

    class Meta:
        model = Receita
        fields = ('id', 'nome_receita', 'informações_adicionais', 'custo_receita', 'rendimento', 'valor_por_produto', 'ingredientes', 'embalagens')
        export_order = ('id', 'nome_receita', 'informações_adicionais', 'custo_receita', 'rendimento', 'valor_por_produto', 'ingredientes', 'embalagens')

    def dehydrate_ingredientes(self, receita):
        return ', '.join([f"{ingrediente.materia_prima.nome_materia_prima} - {ingrediente.quantidade}" for ingrediente in receita.ingredientes_set.all()])

    def dehydrate_embalagens(self, receita):
        return ', '.join([f"{embalagem.embalagem} - {embalagem.quantidade}" for embalagem in receita.embalagens_set.all()])


class IngredientesImportResource(resources.ModelResource):
    receita = fields.Field(
        column_name='receita',
        attribute='receita',
        widget=ForeignKeyWidget(Receita, 'nome_receita')
    )

    materia_prima = fields.Field(
        column_name='materia_prima',
        attribute='materia_prima',
        widget=ForeignKeyWidget(MateriaPrima, 'nome_materia_prima')
    )

    quantidade = fields.Field(
        column_name='quantidade',
        attribute='quantidade'
    )

    valor_total = fields.Field(
        column_name='valor_total',
        attribute='valor_total'
    )

    class Meta:
        model = Ingredientes
        import_id_fields = ('id',)
        fields = ('id', 'receita', 'materia_prima', 'quantidade', 'valor_total')
        export_order = ('id', 'receita', 'materia_prima', 'quantidade', 'valor_total')

class EmbalagensImportResource(resources.ModelResource):
    receita = fields.Field(
        column_name='receita',
        attribute='receita',
        widget=ForeignKeyWidget(Receita, 'nome_receita')
    )

    embalagem = fields.Field(
        column_name='embalagem',
        attribute='embalagem'
    )

    nome_tipo_embalagem = fields.Field(
        column_name='nome_tipo_embalagem',
        attribute='nome_tipo_embalagem',
        widget=ForeignKeyWidget(TipoEmbalagem, 'nome_tipo_embalagem')
    )

    quantidade = fields.Field(
        column_name='quantidade',
        attribute='quantidade'
    )

    valor_embalagem = fields.Field(
        column_name='valor_embalagem',
        attribute='valor_embalagem'
    )

    valor_total = fields.Field(
        column_name='valor_total',
        attribute='valor_total'
    )

    class Meta:
        model = Embalagens
        import_id_fields = ('id',)
        fields = ('id', 'receita', 'embalagem', 'nome_tipo_embalagem', 'quantidade', 'valor_embalagem', 'valor_total')
        export_order = ('id', 'receita', 'embalagem', 'nome_tipo_embalagem', 'quantidade', 'valor_embalagem', 'valor_total')


class ReceitaImportResource(resources.ModelResource):
    ingredientes = fields.Field(
        column_name='ingredientes',
        attribute='ingredientes',
        widget=ForeignKeyWidget(Ingredientes, 'materia_prima__nome_materia_prima')
    )

    embalagens = fields.Field(
        column_name='embalagens',
        attribute='embalagens',
        widget=ForeignKeyWidget(Embalagens, 'embalagem')
    )

    class Meta:
        model = Receita
        import_id_fields = ('id',)
        fields = ('id', 'nome_receita', 'informações_adicionais', 'custo_receita', 'rendimento', 'valor_por_produto', 'ingredientes', 'embalagens')
        export_order = ('id', 'nome_receita', 'informações_adicionais', 'custo_receita', 'rendimento', 'valor_por_produto', 'ingredientes', 'embalagens')
