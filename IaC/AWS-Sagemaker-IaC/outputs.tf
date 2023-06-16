output "endpoint_arn_output" {
  value = module.sagemaker[*].endpoint_arn
}