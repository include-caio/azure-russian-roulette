import subprocess, sys, random, time
from azure.identity import AzureCliCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient

def is_logged_in():
    try:
        subprocess.check_output(["az", "account", "show"])
        return True
    except subprocess.CalledProcessError:
        return False
    
if (not(is_logged_in())):
    print('Conecte na sua conta com o "az login" antes de continuar')
    sys.exit()

credential = AzureCliCredential()
subscription_client = SubscriptionClient(credential)
subscriptions = subscription_client.subscriptions.list()
active_subscriptions = [sub for sub in subscriptions if sub.state == 'Enabled']

subscription_id = active_subscriptions[0].subscription_id

resource_client = ResourceManagementClient(credential, subscription_id)
resource_groups = resource_client.resource_groups.list()
resource_group = next(iter(resource_groups))
resource_group_name = resource_group.name

print(f"Alvo: Subscription Id: {subscription_id} | Resource Group: {resource_group_name}")

print(f"Será que hoje é seu dia de sorte?")
time.sleep(7)

if (random.randint(1, 6) == 3):
    print(f"Não é seu dia de sorte. Deletando Resource Group: {resource_group_name}")
    resource_client.resource_groups.begin_delete(resource_group_name)
else:
    print("Parabéns")