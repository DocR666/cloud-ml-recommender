output "resource_group_name" { value = module.resource_group.name }
output "storage_account_name" { value = module.storage.account_name }
output "model_container_name" { value = module.storage.container_name }
output "acr_name" { value = module.registry.name }
output "acr_login_server" { value = module.registry.login_server }
output "api_url" { value = module.container_app.url }