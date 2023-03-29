# from time import sleep
#
# from tests.test_app.model.proxies import current_service as multilignaul_service
# from invenio_access.permissions import system_identity
#
#
# def test_create(app, db):
#     rec = multilignaul_service.create(system_identity,
#             {
#                 "metadata": {
#                     "a": [{"lang": "cs", "value": "zaznam"},
#                           {"lang": "en", "value": "record"}]
#                 }
#
#
#
#             },)
#     assert len(rec.data) == 6
#     assert len(rec.errors) == 0
#
#     sleep(2)
#     lang_facet = multilignaul_service.scan(system_identity, params={'facets': {'a_lang': ["cs"]}})
#     special_facet = multilignaul_service.scan(system_identity, params={'facets': {'a_cs_keyword': ["zaznam"]}})
#
#     assert len(list(lang_facet.hits)) == 1
#     assert len(list(special_facet.hits)) == 1