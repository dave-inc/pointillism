from prmonster.db import Connection

CONN = Connection()

# class TestDb:
#     def test_init(self):
#         CONN.execute("""
#         CREATE TABLE leads (
#             repo text,
#             contact text,
#             dots real,
#             refs real,
#             status text,
#             notes text
#         );""")
#
#     # def test_insert(self):
#     #     CONN.execute("""
#     #     INSERT
#     #     """)
