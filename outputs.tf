output "app_id" {
  value = { for k, v in module.rg : k => v.app_id }
}
