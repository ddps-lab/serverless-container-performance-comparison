output "cloudfunction_url" {
  value = google_cloudfunctions_function.cloudfunctions_function.https_trigger_url
}
