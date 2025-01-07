from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
 
class OrdemProducaoProdutoInline(admin.TabularInline):
    model = OrdemProducaoProduto
    extra = 1


class EntradaProdutoItemInline(admin.TabularInline):
    model = EntradaProdutoItem
    extra = 1

class SaidaProdutoItemInline(admin.TabularInline):
    model = SaidaProdutoItem
    extra = 1

class ImpostosInline(admin.TabularInline):
    model = Impostos
    extra = 1

class IngredientesInline(admin.TabularInline):
    model = Ingredientes
    readonly_fields = ('valor_total',)
    extra = 1

class EmbalagensInline(admin.TabularInline):
    model = Embalagens
    extra = 1
    readonly_fields = ('valor_total',)

class ProducaoFuncionarioInline(admin.TabularInline):
    model = ProducaoFuncionario
    extra = 1
    readonly_fields = ('valor_da_execucao',)

class ReceitaAdmin(admin.ModelAdmin):
    readonly_fields = ['custo_receita']

    def custo_total_ingredientes(self, obj):
        return sum(ingrediente.valor_total for ingrediente in obj.ingredientes_set.all() if ingrediente.valor_total is not None)

    def custo_total_producao_funcionario(self, obj):
        return sum(execucao.valor_da_execucao for execucao in obj.execucao_mao_de_obra_set.all() if execucao.valor_da_execucao is not None)
    
    def lucro(self, obj):
        return obj.valor_por_produto - self.custo_receita(obj)
    
    def embalagem(self, obj):
        return sum(embalagem.valor_total for embalagem in obj.embalagens_set.all() if embalagem.valor_total is not None)

    def custo_receita(self, obj):
        custo_total = self.custo_total_ingredientes(obj) + self.custo_total_mao_de_obra(obj)
        return custo_total

    custo_receita.short_description = 'Custo Total'

    list_display = ['nome_receita', 'custo_receita', 'custo_total_producao_funcionario', 'custo_total_ingredientes']
    

    inlines = [IngredientesInline,  ProducaoFuncionarioInline, EmbalagensInline, ImpostosInline]

class SubCentroDeCustoInline(admin.TabularInline):
    model = SubCentroDeCusto
    extra = 1

class CustoGeralAdmin(admin.ModelAdmin):
    list_display = ['custo_final', 'custo_indireto_por_unidade','formatted_numero_de_itens']
    list_display_links = ['custo_final']
    inlines = [SubCentroDeCustoInline]
    readonly_fields = ['custo_final', 'custo_indireto_por_unidade', 'numero_de_itens', ]

    def formatted_numero_de_itens(self, obj):
        if obj.data_inicio and obj.data_fim:
            data_inicio_formatada = obj.data_inicio.strftime('%d/%m/%Y')
            data_fim_formatada = obj.data_fim.strftime('%d/%m/%Y')
            return f'{obj.numero_de_itens} Itens produzidos Entre {data_inicio_formatada} e {data_fim_formatada}'
        return obj.numero_de_itens
    formatted_numero_de_itens.short_description = 'Número de Itens'


class SubCentroDeCustoInlineReadOnly(admin.TabularInline):
    model = SubCentroDeCusto
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

class CustoGeralReadOnlyAdmin(admin.ModelAdmin):
    list_display = ['receita', 'custo_final', 'custo_indireto_por_unidade', 'numero_de_itens', ]
    inlines = [SubCentroDeCustoInlineReadOnly]
    list_display_links = ['receita']
    readonly_fields = ['detalhes_receita']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def detalhes_receita(self, obj):
        receita = obj.receita
        ingredientes = receita.ingredientes_set.all()
        embalagens = receita.embalagens_set.all()
        execucoes = receita.execucao_mao_de_obra_set.all()
        impostos = receita.impostos_set.all()

        detalhes = f"Receita: {receita.nome_receita.nome_produto}\n"
        detalhes += f"Informações Adicionais: {receita.informações_adicionais}\n"
        detalhes += f"Custo Receita: {receita.custo_receita}\n\n"

        detalhes += "Ingredientes:\n"
        for ingrediente in ingredientes:
            detalhes += f"- {ingrediente.materia_prima.nome_materia_prima}: {ingrediente.quantidade} unidades, Valor Total: {ingrediente.valor_total}\n"

        detalhes += "\nEmbalagens:\n"
        for embalagem in embalagens:
            detalhes += f"- {embalagem.embalagem}: -{embalagem.nome_tipo_embalagem}: {embalagem.quantidade} unidades, Valor Total: {embalagem.valor_total}\n"

        detalhes += "\nExecução de Mão de Obra:\n"
        for execucao in execucoes:
            detalhes += f"- {execucao.etapa_producao.atividade_servico}: {execucao.tempo_gasto} horas, Valor da Execução: {execucao.valor_da_execucao}\n"

        detalhes += "\nImpostos:\n"
        for imposto in impostos:
            detalhes += f"- {imposto.nome_imposto}: Valor do Imposto: {imposto.valor_imposto}\n"

        return detalhes

    detalhes_receita.short_description = 'Detalhes da Receita'


class OrdemProducaoAdmin(admin.ModelAdmin):
    inlines = [OrdemProducaoProdutoInline]
    exclude = ['produto']

class EntradaProdutoAdmin(admin.ModelAdmin):
    inlines = [EntradaProdutoItemInline]  

class SaidaProdutoAdmin(admin.ModelAdmin):
    inlines = [SaidaProdutoItemInline]
    date_hierarchy = 'data_hora'
    

class HistoricoPrecoAdmin(admin.ModelAdmin):
    readonly_fields = ('preco_anterior', 'preco_atual', 'data_modificacao', 'produto', 'origem')


class ProdutoAdmin(ImportExportModelAdmin):
    list_display = ['nome_produto', 'preco_produto', 'tipo', 'marca', 'fabricante']
    list_display_links = ['nome_produto']
    list_filter = ['tipo', 'marca', 'fabricante',]
    list_editable = ['preco_produto']
    search_fields = ['nome_produto']
    list_per_page = 10
    readonly_fields = ('lucro',)
    exclude = ['lucro']
 

admin.site.register(Funcionario)
admin.site.register(GrupoCategoria)
admin.site.register(SubgrupoSubcategoria)
admin.site.register(Marca)
admin.site.register(Fabricante)
admin.site.register(Tipo)
admin.site.register(UnidadeMedida)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(AtividadeServico)
admin.site.register(Receita, ReceitaAdmin)
admin.site.register(OrdemProducao, OrdemProducaoAdmin)
admin.site.register(Destinatario)
admin.site.register(EntradaProduto, EntradaProdutoAdmin)
admin.site.register(SaidaProduto, SaidaProdutoAdmin)
admin.site.register(TesteQualidade)
admin.site.register(Setor)
admin.site.register(MateriaPrima)
admin.site.register(SubCentroDeCusto)
admin.site.register(HistoricoPreco, HistoricoPrecoAdmin)
admin.site.register(CentroDeCusto)
admin.site.register(TipoEmbalagem)
admin.site.register(Embalagens)
admin.site.register(Ingredientes)
admin.site.register(CustoGeral, CustoGeralAdmin)
admin.site.register(CustoGeralReadOnly, CustoGeralReadOnlyAdmin)
