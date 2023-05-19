# policy_data = data.google_iam_policy.noauth.policy_data

module "cloudfunction" {
  count         = length(var.enabled_models)
  source        = "./cloudfunction"
  region        = var.region
  model_name    = var.enabled_models[count.index]
  bucket_name   = var.bucket_name
  ram_mib       = var.model_resources[var.enabled_models[count.index]].ram_mib
  min_instances = var.model_resources[var.enabled_models[count.index]].min_instances
  max_instances = var.model_resources[var.enabled_models[count.index]].max_instances
}
