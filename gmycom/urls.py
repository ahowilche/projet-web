from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('login/', views.agent_login, name='login'),
    path('logout/', views.agent_logout, name='logout'),

    # Tableau de bord
    path('dashboard/', views.dashboard, name='dashboard'),

    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_update, name='client_update'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'), 
    path('client/<int:pk>/pdf/', views.client_pdf_view, name='client_pdf'),

    # Comptes
    path('comptes/', views.compte_list, name='compte_list'),
    path('ajax/search-clients/', views.search_clients_ajax, name='search_clients_ajax'),
    path('comptes/new/', views.compte_create, name='compte_create'),
    path('clients/<int:client_id>/comptes/new/', views.compte_create, name='compte_create_for_client'), # Créer un compte depuis un client
    path('comptes/<int:pk>/', views.compte_detail, name='compte_detail'),
    path('comptes/<int:pk>/delete/', views.compte_delete, name='compte_delete'),


    # Mouvements (Dépôt/Retrait/Virement)
    path('ajax/search-comptes/', views.search_comptes_ajax, name='search_comptes_ajax'),
    path('mouvements/new/', views.mouvement_create, name='mouvement_create'),
    path('comptes/<int:compte_id>/mouvements/new/', views.mouvement_create, name='mouvement_create_for_compte'), # Créer un mouvement depuis un compte

    # Historique des transactions (nouvelle URL)
    path('transactions/history/', views.transaction_history_list, name='transaction_history_list'),

    # Crédits
    path('credits/', views.credit_list, name='credit_list'),
    path('credits/new/', views.credit_create, name='credit_create'),
    path('clients/<int:client_id>/credits/new/', views.credit_create, name='credit_create_for_client'), # Créer un crédit depuis un client
    path('credits/<int:pk>/', views.credit_detail, name='credit_detail'),
    path('ajax/get-compte-details/', views.get_compte_details, name='get_compte_details'),
    path('credits/search_ajax/', views.credit_search_ajax, name='credit_search_ajax'),
    
    # Remboursements
    path('remboursements/new/', views.remboursement_create, name='remboursement_create'),
    path('credits/<int:credit_id>/remboursements/new/', views.remboursement_create, name='remboursement_create_for_credit'), # Créer un remboursement depuis un crédit

    # Rapports
    path('reports/situation/', views.situation_report, name='situation_report'),

    path('credits/get_details_ajax/', views.get_credit_details_ajax, name='get_credit_details_ajax'),
    path('credits/<int:pk>/repayments_ajax/', views.get_repayments_ajax, name='repayments_ajax'),
]
