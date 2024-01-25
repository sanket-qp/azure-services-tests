import time
import common

import pytest
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient


@pytest.mark.encryption
class TestPostgresEncryption:
    def test_key_rotation(self, ddl_user_connection):
        """
        Verifies data retrieval after key rotation
        """
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]

        # Rotate keys using Azure sdk
        token_credential = DefaultAzureCredential()

        VAULT_URL = "https://sp-westus2-keyvault.vault.azure.net/"
        client = KeyClient(vault_url=VAULT_URL, credential=token_credential)
        keys = client.list_properties_of_keys()
        
        rtn = client.rotate_key('sp-westus2-keyvault-key')
        print (rtn)

        
        # Query again
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]