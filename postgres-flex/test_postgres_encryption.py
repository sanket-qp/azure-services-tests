import time
from datetime import datetime
from datetime import timezone
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
        # Verify prerequisites
        vault_url = common.get_key_vault_url()
        assert vault_url is not None, "VAULT_URL must be set"

        key_name = common.get_key_valult_key_name()
        assert key_name is not None, "KEY_NAME must be set"

        # Query existing data
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]

        # Rotate keys using Azure sdk
        token_credential = DefaultAzureCredential()
        time_before_rotation = datetime.now(tz=timezone.utc)
        print ("created", time_before_rotation)
        client = KeyClient(vault_url=vault_url, credential=token_credential)
        key = client.get_key(key_name)
        assert key is not None
        old_version = key.properties.version
        print ("old_version", old_version)
        time.sleep(5)
        key = client.rotate_key('sp-westus2-keyvault-key')
        assert key is not None
        time.sleep(5)
        new_version = key.properties.version
        print ("new_version", new_version)
        assert new_version != old_version
        print ("updated", key.properties.updated_on)
        assert key.properties.updated_on > time_before_rotation

        # Query again
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]