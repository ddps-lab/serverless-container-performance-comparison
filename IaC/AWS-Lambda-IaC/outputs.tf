output "api_gateway_url_output" {
  value = module.lambda[*].api_gateway_url
}