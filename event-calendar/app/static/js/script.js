$(document).ready(function () {
    $('#example').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        order: [[0, 'asc']],
        stateSave: true,
        responsive: true,
        fixedHeader: true,
        fixedColumns: true,
        rowGroup: true,
        dom: 'Bfrtip',
                buttons: [
                    {
                        extend: 'collection',
                        text: 'Exportar ...',
                        buttons: [
                            {
                                extend: 'excel',
                                text: 'Exportar para Excel',
                                exportOptions: {
                                    columns: [0, 1, 2, 3, 4, 5, 6, 7] // Índices das colunas que serão exportadas
                                }
                            },
                            {
                                extend: 'pdf',
                                text: 'Exportar para PDF',
                                exportOptions: {
                                    columns: [0, 1, 2, 3, 4, 5, 6, 7] // Índices das colunas que serão exportadas
        
                                }
                            },
                            {
                                extend: 'print',
                                text: 'Imprimir',
                                exportOptions: {
                                    columns: [0, 1, 2, 3, 4, 5, 6, 7] // Índices das colunas que serão exportadas
                                }
                            },
                        ]
                    },
                    {
                        extend: 'colvis',
                    },
                    {
                        extend: 'pageLength',
                    },
                    {
                        extend: 'searchBuilder',
                        text: 'Filtrar'
                    },
                    
                    
                ]
            }
        
    );


    setTimeout(function () {
        $("#message").alert('close');
    }, 3000);

    $('.inlineform').each(function () {
        var lastMb3 = $(this).find('.row .mb-3:last');
        lastMb3.hide();
    });

    $('.inlineform-produto').each(function () {
        var lastMb3 = $(this).find('.row .mb-3:last');
        lastMb3.hide();
    });
});
        

    
