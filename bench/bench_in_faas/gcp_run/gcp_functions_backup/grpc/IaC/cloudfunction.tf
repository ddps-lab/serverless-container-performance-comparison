resource "google_cloudfunctions_function" "cloudfunctions_function" {
  name                         = "${var.prefix}-scpc-grpc-bench"
  region                       = var.region
  runtime                      = "python310"
  source_archive_bucket        = var.bucket_name
  source_archive_object        = "scpc_grpc_bench.zip"
  entry_point                  = "function_handler"
  available_memory_mb          = 4096
  min_instances                = 0
  max_instances                = 300
  timeout                      = 120
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"
  environment_variables = {
    AWS_ACCESS_KEY_ID     = var.aws_access_key
    AWS_SECRET_ACCESS_KEY = var.aws_secret_access_key
    AWS_REGION            = var.aws_region
  }
  timeouts {
    create = "15m"
    update = "15m"
  }
}

resource "google_cloudfunctions_function_iam_member" "cloudfunction_noauth" {
  region         = google_cloudfunctions_function.cloudfunctions_function.region
  project        = google_cloudfunctions_function.cloudfunctions_function.project
  cloud_function = google_cloudfunctions_function.cloudfunctions_function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}
