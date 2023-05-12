output "mobilenet_v1_output" {
  value = module.cloudrun[*].cloudrun_url
}