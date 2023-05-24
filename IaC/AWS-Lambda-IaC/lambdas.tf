resource "aws_s3_bucket" "bucket" {
  bucket = "${var.prefix}-scpc-bucket"
  force_destroy = true
}

module "lambda" {
  count           = length(var.enabled_models)
  source          = "./lambda"
  prefix          = var.prefix
  docker_registry = var.docker_registry
  route53_zoneid  = data.aws_route53_zone.route53_zone.zone_id
  route53_domain  = var.route53_domain
  model_name      = var.enabled_models[count.index]
  ram_mib         = var.model_resources[var.enabled_models[count.index]].ram_mib
}
