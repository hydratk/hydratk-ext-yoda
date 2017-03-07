# -*- coding: utf-8 -*-

"""This code is a part of Yoda Extension

.. module:: hydratk.extensions.yoda.translation.cs
   :platform: Unix
   :synopsis: Czech language translation for Yoda extension
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 


msg = {
    'yoda_start_test_from'                     : ["Spouštím testy z adresáře: {0}"],
    'yoda_test_repo_root_override'             : ["Přepisuji test_repo_root directory s: {0}"],
    'yoda_invalid_test_base_path'              : ["Špatný základní adresář testů: {0}"],
    'yoda_invalid_test_repo_root'              : ["Špatný kořenový adresář repositáře: {0}"],
    'yoda_added_helpers_dir'                   : ["Přidán adresář pomocných knihoven {0}"],
    'yoda_helpers_dir_not_exists'              : ["Adresář pomocných knihoven {0} neexistuje, vynecháno"],
    'yoda_added_lib_dir'                       : ["Přidán adresář sdílených knihoven {0}"],
    'yoda_lib_dir_not_exists'                  : ["Adresář sdílených knihoven {0} neexistuje, vynecháno"], 
    'yoda_process_test_sets_total'             : ["Nalezeno {0} test setů pro zpracování"],
    'yoda_no_tests_found_in_path'              : ["Nebyly nalezeny žádné testy ve složce: {0}"],
    'yoda_process_test_set'                    : ["Zpracovávám test set: {0}"],
    'yoda_test_run_summary'                    : ["Testovací Běh: test sety: {0}, testy - celkem: {1}, chybné: {2}, úspěšné: {3}"],
    'yoda_test_set_summary'                    : ["Test Set: {0}"],
    'yoda_test_scenario_summary'               : ["Test. Scénář: {0}, testy - celkem: {1}, chybné: {2}, úspěšné: {3}"],
    'yoda_test_scenario_prereq_passed'         : ["Předtestovací požadavky úspěšně splněny"],
    'yoda_test_scenario_prereq_failed'         : ["Předtestovací požadavky selhaly: \n{0}"],
    'yoda_test_scenario_postreq_failed'        : ["Post-požadavky selhaly: {0}"],
    'yoda_test_scenario_postreq_passed'        : ["Post-požadavky úspěšně splňeny"],    
    'yoda_test_scenario_events_failed'         : ["Vyskytnuly se problémy v událostech test. scénáře: \n{0}"],
    'yoda_test_case_events_failed'             : ["Vyskytnuly se problémy v událostech test. případu: \n{0}"],
    'yoda_test_condition_events_failed'        : ["Vyskytnuly se problémy v událostech test. podmínky: \n{0}"],
    'yoda_test_condition_test_exec_failed'     : ["Vyskytnuly se problémy během spuštění testu: \n{0}"],
    'yoda_test_condition_validate_exec_failed' : ["Vyskytnuly se problémy během vyhodnocení testu: \n{0}"],
    'yoda_test_case'                           : ["Test. Případ: {0}"],
    'yoda_test_condition'                      : ["Test. Podmínka: {0}"],
    'yoda_expected_result'                     : ["Očekávaný Výsledek: {0}"],
    'yoda_actual_result'                       : ["Aktuální Výsledek: {0}"],
    'yoda_log'                                 : ["Log: {0}"],
    'yoda_parsing_test_scenario'               : ["Parsuji atributy Test-Scenario {0}={1}"],
    'yoda_parsing_test_case'                   : ["Parsuji atributy Test-Case {0}={1}"],
    'yoda_parsing_test_condition'              : ["Parsuji atributy Test-Condition {0}={1}"],
    'yoda_scenario_tag_expected'               : ["Očekáván tag Test-Scenario-{0}"],
    'yoda_wrong_tset_structure'                : ["Nevalidní struktura test setu"],
    'yoda_inline_loop_detected'                : ["Detekována smyčka vnořených testů {0}"],
    'yoda_inline_test_exec'                    : ["Spouštím vnořený test: {0}"],
    'yoda_running_tset_global'                 : ["Spouštím globální test set {0}"],
    'yoda_running_tset_repo'                   : ["Spouštím test sety z repozitáře: {0}"],
    'yoda_create_tset_db'                      : ["Vytvářím databázový záznam pro test set {0}"],
    'yoda_create_tset_db_error'                : ["Nastala chyba při vytváření databázového záznamu pro test set"],
    'yoda_update_tset_db_error'                : ["Nastala chyba při editaci databázového záznamu pro test set"],
    'yoda_parsing_container'                   : ["Parsuji soubor kontejneru testů: {0}"],
    'yoda_processing_container'                : ["Zpracovávám obsah kontejneru testů: {0}"],
    'yoda_getting_tests'                       : ["Beru testy na cestě: {0}"],
    'yoda_filter_parameters'                   : ["Parametry filtru:\n\ttest_path: {0}\n\tts_filter: {1}\n\ttca_filter: {2}\n\ttco_filter: {3}"],
    'yoda_unknown_test_path'                   : ["Cesta k testu {0} neexistuje"],
    'yoda_unsupported_extension'               : ["Nepodporovaná přípona souboru: {0} v {1}"],
    'yoda_create_test_run_db_error'            : ["Nastala chyba při vytváření databázového záznamu pro test run"],
    'yoda_update_test_run_db_error'            : ["Nastala chyba při editaci databázového záznamu pro test run"],
    'yoda_create_test_set_db'                  : ["Vytvářím databázový záznam pro test set {0}"],     
    'yoda_create_test_set_db_error'            : ["Nastala chyba při vytváření databázového záznamu pro test set"],
    'yoda_update_test_set_db_error'            : ["Nastala chyba při editaci databázového záznamu pro test set"],
    'yoda_create_test_scenario_db_error'       : ["Nastala chyba při vytváření databázového záznamu pro test scenario"],
    'yoda_update_test_scenario_db_error'       : ["Nastala chyba při editaci databázového záznamu pro test scenario"],
    'yoda_create_test_case_db_error'           : ["Nastala chyba při vytváření databázového záznamu pro test case"],
    'yoda_update_test_case_db_error'           : ["Nastala chyba při editaci databázového záznamu pro test case"],
    'yoda_create_test_condition_db_error'      : ["Nastala chyba při vytváření databázového záznamu pro test condition"],
    'yoda_update_test_condition_db_error'      : ["Nastala chyba při editaci databázového záznamu pro test condition"],    
    'yoda_skipping_test_scenario'              : ["Filtr: Přeskakuji testovací scénář {0}"],
    'yoda_skipping_test_case'                  : ["Filtr: Přeskakuji testovací případ {0}"],
    'yoda_skipping_test_condition'             : ["Filtr: Přeskakuji testovací podmínku {0}"],
    'yoda_simulating_test_scenario'            : ["Simulace: Spouštím Test scenario {0} pre-req"],
    'yoda_simulating_test_scenario_before'     : ["Simulace: Spouštím Test scenario {0} yoda_events_before_start_ts"],
    'yoda_simulating_test_scenario_after'      : ["Simulace: Spouštím Test scenario {0} yoda_events_after_finish_ts"],
    'yoda_simulating_test_scenario_postreq'    : ["Simulace: Spouštím Test scenario {0} post-req"],
    'yoda_simulating_test_case'                : ["Simulace: Spouštím Test case: {0}, Test condition: {1}"],
    'yoda_simulating_test_case_before'         : ["Simulace: Spouštím Test Case {0} yoda_events_before_start_tca"],
    'yoda_simulating_test_case_after'          : ["Simulace: Spouštím Test Case {0} yoda_events_after_finish_tca"],
    'yoda_simulating_test_condition_before'    : ["Simulace: Spouštím Test Condition {0} yoda_events_before_start_tco"],
    'yoda_simulating_test_condition_after'     : ["Simulace: Spouštím Test Condition {0} yoda_events_after_finish_tco"],
    'yoda_simulating_validation'               : ["Simulace: Validuji výsledek, Test case: {0}, Test condition: {1}"],      
    'yoda_break_outside'                       : ["Nelze použít '{0}' mimo sekci {1}"],
    'yoda_registering_actions'                 : ["Registruji {0} akce"],
    'yoda_context_switch'                      : ["Získán context switch, aktivní tikety: {0}"],
    'yoda_checking_ticket'                     : ["Kontroluji tiket id {0}"],
    'yoda_waiting_tickets'                     : ["Čekající tikety {0}"],
    'yoda_create_db'                           : ["Vytvářím databázi výsledků testů s dsn: {0}"],
    'yoda_test_results_output_override'        : ["Přepisuji nastavení výstupu testů s: {0}"],
    'yoda_test_results_handler_override'       : ["Přepisuji handler výstupů testů s: {0}"],
    'yoda_test_results_db_override'            : ["Přepisuji dsn databáze výsledků testů s: {0}"],
    'yoda_test_results_db_init'                : ["Inicializuji datavází výsledků testů s dsn: {0}"],
    'yoda_test_results_db_check_fail'          : ["Kontrola databáze výsledků testů s dsn: {0} provedena neúspěšně"],
    'yoda_test_results_db_check_ok'            : ["Kontrola databáze výsledků testů s dsn: {0} provedena úspěšně."],
    'yoda_processing_tests'                    : ["Zpracovávám testy test_simul_mode {0}, run_mode {1}"],
    'yoda_received_break'                      : ["Zachycen break {0}"],
    'yoda_processing_tset'                     : ["Zpracovávám test set {0}"],
    'yoda_processing_tset_parallel'            : ["Zpracovávám test set {0} v paralelním režimu"],
    'yoda_got_ticket'                          : ["Získán tiket id: {0} pro test set: {1}"],
    'yoda_test_results_db_missing'             : ["Databáze výsledků testů neexistuje"],
    'yoda_db_exists'                           : ["Databáze s dsn:{0} již existuje"],
    'yoda_db_created'                          : ["Databáze úspěšně vytvořena"],
    'yoda_running_action'                      : ["Spouštím akci: {0} {1}"], 
    'yoda_getting_action_data'                 : ["Získána data pro akci: {0} {1}"],
    'yoda_unknown_handler'                     : ["Neznámý handler: {0}"],
    'yoda_create_output_console'               : ["Vytvářím výstup testů na konzoli"],
    'yoda_create_output_html'                  : ["Vytvářím výstup testů soubor html: {0}"],
    'yoda_create_testdata_db'                  : ["Vytvářím databázi testovacích dat s dsn: {0}"],
    'yoda_remove_testdata_db'                  : ["Mažu fatabázi testovacích dat s dsn: {0}"],
    'yoda_testdata_db_exists'                  : ["Databáze testovacích dat s dsn: {0} již existuje"],
    'yoda_testdata_db_created'                 : ["Databáze testovacích dat úspěšně vytvořena"],
    'yoda_testdata_db_error'                   : ["Nastala chyb při vytváření databáze testovacích dat: {0}"],
    'yoda_multiply_tests'                      : ["Celkový počet test setů po vynásobení je: {0}"]                                   
}