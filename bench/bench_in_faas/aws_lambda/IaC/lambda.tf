resource "aws_iam_role" "lambda-role" {
  name = "${var.prefix}-aws-lambda-scpc-bench-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_policy" {
  role       = aws_iam_role.lambda-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_S3_policy" {
  role       = aws_iam_role.lambda-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "lambda" {
  function_name = "${var.prefix}-aws-lambda-scpc-bench"
  package_type  = "Image"
  architectures = ["x86_64"]
  image_uri     = "${var.docker_registry}/${var.docker_image_tag}"
  memory_size   = 4096
  timeout       = 120
  role          = aws_iam_role.lambda-role.arn
}

resource "aws_cloudwatch_log_group" "lambda-cloudwath-log-group" {
  name = "/aws/lambda/${aws_lambda_function.lambda.function_name}"

  retention_in_days = 30
}

resource "aws_apigatewayv2_api" "lambda-api" {
  name          = "${var.prefix}-aws-lambda-scpc-bench-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda-api-stage" {
  api_id      = aws_apigatewayv2_api.lambda-api.id
  name        = "${var.prefix}-aws-lambda-scpc-bench-api-stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_cloudwatch_log_group.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "lambda-api-execution" {
  api_id = aws_apigatewayv2_api.lambda-api.id

  integration_uri    = aws_lambda_function.lambda.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "api_gw_route" {
  api_id = aws_apigatewayv2_api.lambda-api.id

  route_key = "POST /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda-api-execution.id}"
}


resource "aws_cloudwatch_log_group" "api_gw_cloudwatch_log_group" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda-api.name}"

  retention_in_days = 30
}


resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda-api.execution_arn}/*/*"
}

resource "aws_acm_certificate" "certificate" {
  domain_name       = "scpcbench.${var.prefix}.${var.route53_domain}"
  validation_method = "DNS"
}

resource "aws_route53_record" "validation_record" {
  for_each = {
    for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.route53_zone.id
}

resource "aws_acm_certificate_validation" "certificate_validation" {
  certificate_arn = aws_acm_certificate.certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.validation_record : record.fqdn]
}

resource "aws_apigatewayv2_domain_name" "api_domain_name" {
  domain_name = "scpcbench.${var.prefix}.${var.route53_domain}"

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.certificate.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  depends_on = [ aws_acm_certificate_validation.certificate_validation ]
}

resource "aws_route53_record" "route53_record" {
  name    = aws_apigatewayv2_domain_name.api_domain_name.domain_name
  type    = "A"
  zone_id = data.aws_route53_zone.route53_zone.id

  alias {
    name                   = aws_apigatewayv2_domain_name.api_domain_name.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api_domain_name.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_apigatewayv2_api_mapping" "api_mapping" {
  api_id = aws_apigatewayv2_api.lambda-api.id
  domain_name = aws_apigatewayv2_domain_name.api_domain_name.id
  stage = aws_apigatewayv2_stage.lambda-api-stage.id
}