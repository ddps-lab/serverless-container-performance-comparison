# policy_data = data.google_iam_policy.noauth.policy_data

module "cloudrun" {
  count           = length(var.enabled_models)
  source          = "./cloudrun"
  region          = var.region
  model_name      = var.enabled_models[count.index]
  docker_registry = var.docker_registry
  cpu_number      = var.model_resources[var.enabled_models[count.index]].cpu_number
  ram_mib         = var.model_resources[var.enabled_models[count.index]].ram_mib
  min_instances   = var.model_resources[var.enabled_models[count.index]].min_instances
  max_instances   = var.model_resources[var.enabled_models[count.index]].max_instances
  noauth_policy   = data.google_iam_policy.noauth.policy_data
}
