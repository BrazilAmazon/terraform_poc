module "rg" {
  source  = "app.terraform.io/ddi-support/rg/azurerm"
  version = "1.0.1"
  rgname = var.rgname
  rglocation = var.rglocation
  planname = var.planname
  kind = var.kind
  # insert required variables here
}
