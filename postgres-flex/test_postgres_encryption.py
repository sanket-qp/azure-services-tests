import time
from datetime import datetime
from datetime import timezone
import common
import pprint

import pytest
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient


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

        subscription_id = common.get_subscription_id()
        assert subscription_id is not None, "SUBSCRIPTION_ID must be set"

        resource_group_name = common.get_resource_group_name()
        assert resource_group_name is not None, "RESOURCE_GROUP_NAME must be set"

        postgres_instance_name = common.get_postgres_instance_name()
        assert postgres_instance_name is not None, "POSTGRES_INSTANCE_NAME must be set"

        postgres_instance_identity = common.get_postgres_instance_identity()
        assert postgres_instance_identity is not None, "POSTGRES_INSTANCE_IDENTITY must be set"

        # Query existing data
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]

        # Rotate keys using Azure sdk
        token_credential = DefaultAzureCredential()
        rotated_key = self.rotate_key(vault_url, key_name, token_credential)
        print ("rotated key:", rotated_key)

        # Update the postgres instance with rotated key
        self.update_postgres_key(resource_group_name, postgres_instance_name, subscription_id, postgres_instance_identity, token_credential, rotated_key)

        # Query again
        with ddl_user_connection.cursor() as cur:
            cur.execute(f"SELECT * from {common.get_article_table_name()}")
            rs = cur.fetchall()
            assert 2 == len(rs)
            assert 'hello_postgres' == rs[0][1]
            assert 'hello_redis' == rs[1][1]

    def rotate_key(self, vault_url, key_name, credentials):
        """
        Rotates the key
        """
        time_before_rotation = datetime.now(tz=timezone.utc)
        print ("created", time_before_rotation)
        client = KeyClient(vault_url=vault_url, credential=credentials)
        current_key = client.get_key(key_name)
        assert current_key is not None
        old_version = current_key.properties.version
        print ("old_version", old_version)
        rotated_key = client.rotate_key(key_name)
        assert rotated_key is not None
        time.sleep(2)
        new_version = rotated_key.properties.version
        print ("new_version", new_version)
        assert new_version != old_version
        print ("updated", rotated_key.properties.updated_on)
        ## assert key.properties.updated_on > time_before_rotation
        print (rotated_key.id)
        return rotated_key

    def update_postgres_key(self, resource_group_name, server_name, subscription_id, postgres_instance_identity, credential, new_key):
        """
        Updates postgres instance's encryption key (key encryption key)
        """
        postgres_client = PostgreSQLManagementClient(credential, subscription_id)
        params = {
                "identity": {
                    "type": "UserAssigned",
                    "userAssignedIdentities": {
                        postgres_instance_identity: {},
                    },
                },
                "properties": {
                    "createMode": "Create",
                    "dataEncryption": {
                        "primaryKeyURI": new_key.id,
                        "primaryUserAssignedIdentityId": postgres_instance_identity,
                        "type": "AzureKeyVault"
                    }
                }
        }

        pprint.PrettyPrinter(depth=4).pprint(params)

        resp = postgres_client.servers.begin_update(
            resource_group_name=resource_group_name, 
            server_name=server_name,
            parameters = params,
            ).result()
        
        print ("------------------------")

        print (resp)
