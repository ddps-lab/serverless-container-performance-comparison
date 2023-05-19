resource "google_cloudfunctions_function" "cloudfunctions_function" {
  name     = "function-${replace(var.model_name, "_", "-")}"
  region = var.region
  runtime = "python310"
  source_archive_bucket = var.bucket_name
  source_archive_object = "${var.model_name}.zip"
  entry_point = "predict"
  available_memory_mb = var.ram_mib
  min_instances = var.min_instances
  max_instances = var.max_instances
  timeout = 120
  trigger_http = true
  https_trigger_security_level = "SECURE_ALWAYS"

  timeouts {
    create = "15m"
  }
}

resource "google_cloudfunctions_function_iam_member" "cloudfunction_noauth" {
  region       = google_cloudfunctions_function.cloudfunctions_function.region
  project        = google_cloudfunctions_function.cloudfunctions_function.project
  cloud_function = google_cloudfunctions_function.cloudfunctions_function.name
  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
