output "app_id" {
  value = { for k, v in module.rg.azurerm_service_plan.example : k => v }
}
