resource "aws_sagemaker_model" "model" {
  name               = "${var.prefix}-scpc-${replace(var.model_name, "_", "-")}-model"
  execution_role_arn = var.iam_role

  primary_container {
    image          = var.sagemaker_prebuilt_image
    model_data_url = "s3://${var.model_bucket}/${var.model_name}.tgz"
  }
}

resource "aws_sagemaker_endpoint_configuration" "endpoint_configuration" {
  name = "${var.prefix}-scpc-${replace(var.model_name, "_", "-")}-endpoint-configuration"

  production_variants {
    variant_name = "default"
    model_name   = aws_sagemaker_model.model.name
    serverless_config {
      max_concurrency = var.max_concurrency
      provisioned_concurrency = var.provisioned_concurrency > 0 ? var.provisioned_concurrency : null
      memory_size_in_mb = var.ram_mib
    }
  }
}

resource "aws_sagemaker_endpoint" "endpoint" {
  name                 = "${var.prefix}-${replace(var.model_name, "_", "-")}-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.endpoint_configuration.name
  lifecycle {
    replace_triggered_by = [ aws_sagemaker_endpoint_configuration.endpoint_configuration ]
  }
}
