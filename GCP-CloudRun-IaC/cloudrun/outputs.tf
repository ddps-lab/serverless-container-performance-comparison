output "cloudrun_url" {
  value = google_cloud_run_service.cloudrun_service[*].status[0].url
}