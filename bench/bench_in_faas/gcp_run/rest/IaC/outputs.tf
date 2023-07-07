output "api_gateway_url" {
  value = aws_apigatewayv2_domain_name.api_domain_name.domain_name
}