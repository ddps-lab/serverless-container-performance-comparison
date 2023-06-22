resource "aws_s3_bucket" "bucket" {
  bucket = "${var.prefix}-scpc-sagemaker-bucket"
  force_destroy = true
}

module "sagemaker" {
  count                    = length(var.enabled_models)
  source                   = "./sagemaker"
  prefix                   = var.prefix
  max_concurrency          = var.max_concurrency
  provisioned_concurrency  = var.provisioned_concurrency
  model_bucket             = var.model_bucket
  model_name               = var.enabled_models[count.index]
  sagemaker_prebuilt_image = data.aws_sagemaker_prebuilt_ecr_image.tensorflow-inference
  ram_mib                  = var.model_resources[var.enabled_models[count.index]].ram_mib
  iam_role                 = aws_iam_role.sagemaker-role.arn
}
