output "mobilenet_v1_output" {
  value = tolist(google_cloud_run_service.cloudrun_mobilenet_v1[*].status.url)
}