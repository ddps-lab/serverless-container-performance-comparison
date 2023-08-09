resource "google_cloud_run_service" "cloudrun_service" {
  count    = length(var.APIS)
  name     = "${var.prefix}-${replace(var.model_name, "_", "-")}-${var.APIS[count.index]}"
  location = var.region
  template {
    spec {
      container_concurrency = var.concurrency
      containers {
        image = "${var.docker_registry}/gcp-run-${var.model_name}-${var.APIS[count.index]}"
        ports {
          name           = var.APIS[count.index] == "grpc" ? "h2c" : "http1"
          container_port = var.APIS[count.index] == "grpc" ? 8500 : 8501
          protocol       = "TCP"
        }
        resources {
          limits = {
            cpu    = "${var.cpu_number * 1000}m"
            memory = "${var.ram_mib}Mi"
          }
        }

        env {
          name = "PUSHGATEWAY_ADDRESS"
          value = var.pushgateway_address
        }

        env {
          name = "MODEL_NAME"
          value = var.model_name
        }

        env {
          name = "RAM_SIZE"
          value = var.ram_mib
        }

        startup_probe {
          initial_delay_seconds = 10
          timeout_seconds       = 1
          period_seconds        = 5
          failure_threshold     = 3
          tcp_socket {
            port = var.APIS[count.index] == "grpc" ? 8500 : 8501
          }
        }
      }
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = var.min_instances
        "autoscaling.knative.dev/maxScale" = var.max_instances
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_policy" "cloudrun_noauth" {
  count    = length(var.APIS)
  location = google_cloud_run_service.cloudrun_service[count.index].location
  project  = google_cloud_run_service.cloudrun_service[count.index].project
  service  = google_cloud_run_service.cloudrun_service[count.index].name

  policy_data = var.noauth_policy
}

# resource "google_bigquery_dataset" "dataset" {
#   dataset_id                  = "${var.prefix}_${var.model_name}"
#   friendly_name               = "${var.prefix}_${var.model_name}"
#   location                    = var.region
#   default_table_expiration_ms = 3600000
# }

# resource "google_bigquery_table" "dataset-table" {
#   count               = length(var.APIS)
#   dataset_id          = "${var.prefix}_${var.model_name}"
#   table_id            = var.APIS[count.index]
#   deletion_protection = false
#   depends_on          = [google_bigquery_dataset.dataset]
#   expiration_time     = 0

#   schema              = <<EOF
# [
#   {
#     "mode": "NULLABLE",
#     "name": "logName",
#     "type": "STRING"
#   },
#   {
#     "fields": [
#       {
#         "mode": "NULLABLE",
#         "name": "type",
#         "type": "STRING"
#       },
#       {
#         "fields": [
#           {
#             "mode": "NULLABLE",
#             "name": "revision_name",
#             "type": "STRING"
#           },
#           {
#             "mode": "NULLABLE",
#             "name": "configuration_name",
#             "type": "STRING"
#           },
#           {
#             "mode": "NULLABLE",
#             "name": "service_name",
#             "type": "STRING"
#           },
#           {
#             "mode": "NULLABLE",
#             "name": "location",
#             "type": "STRING"
#           },
#           {
#             "mode": "NULLABLE",
#             "name": "project_id",
#             "type": "STRING"
#           }
#         ],
#         "mode": "NULLABLE",
#         "name": "labels",
#         "type": "RECORD"
#       }
#     ],
#     "mode": "NULLABLE",
#     "name": "resource",
#     "type": "RECORD"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "textPayload",
#     "type": "STRING"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "timestamp",
#     "type": "TIMESTAMP"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "receiveTimestamp",
#     "type": "TIMESTAMP"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "severity",
#     "type": "STRING"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "insertId",
#     "type": "STRING"
#   },
#   {
#     "fields": [
#       {
#         "mode": "NULLABLE",
#         "name": "requestMethod",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "requestUrl",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "requestSize",
#         "type": "INTEGER"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "status",
#         "type": "INTEGER"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "responseSize",
#         "type": "INTEGER"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "userAgent",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "remoteIp",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "serverIp",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "referer",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "latency",
#         "type": "FLOAT"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "cacheLookup",
#         "type": "BOOLEAN"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "cacheHit",
#         "type": "BOOLEAN"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "cacheValidatedWithOriginServer",
#         "type": "BOOLEAN"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "cacheFillBytes",
#         "type": "INTEGER"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "protocol",
#         "type": "STRING"
#       }
#     ],
#     "mode": "NULLABLE",
#     "name": "httpRequest",
#     "type": "RECORD"
#   },
#   {
#     "fields": [
#       {
#         "mode": "NULLABLE",
#         "name": "instanceid",
#         "type": "STRING"
#       }
#     ],
#     "mode": "NULLABLE",
#     "name": "labels",
#     "type": "RECORD"
#   },
#   {
#     "fields": [
#       {
#         "mode": "NULLABLE",
#         "name": "id",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "producer",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "first",
#         "type": "BOOLEAN"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "last",
#         "type": "BOOLEAN"
#       }
#     ],
#     "mode": "NULLABLE",
#     "name": "operation",
#     "type": "RECORD"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "trace",
#     "type": "STRING"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "spanId",
#     "type": "STRING"
#   },
#   {
#     "mode": "NULLABLE",
#     "name": "traceSampled",
#     "type": "BOOLEAN"
#   },
#   {
#     "fields": [
#       {
#         "mode": "NULLABLE",
#         "name": "file",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "line",
#         "type": "INTEGER"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "function",
#         "type": "STRING"
#       }
#     ],
#     "mode": "NULLABLE",
#     "name": "sourceLocation",
#     "type": "RECORD"
#   },
#   {
#     "fields": [
#       {
#         "mode": "NULLABLE",
#         "name": "uid",
#         "type": "STRING"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "index",
#         "type": "INTEGER"
#       },
#       {
#         "mode": "NULLABLE",
#         "name": "totalSplits",
#         "type": "INTEGER"
#       }
#     ],
#     "mode": "NULLABLE",
#     "name": "split",
#     "type": "RECORD"
#   }
# ]
# EOF
# }

# resource "google_logging_project_sink" "logging_sink" {
#   count       = length(var.APIS)
#   name        = "${var.prefix}-${var.model_name}-${var.APIS[count.index]}-sink"
#   destination = "bigquery.googleapis.com/projects/${var.project_name}/datasets/${var.prefix}_${var.model_name}/tables/${var.APIS[count.index]}"

#   filter                 = var.APIS[count.index] == "grpc" ? "httpRequest.status=200 httpRequest.requestUrl=\"${google_cloud_run_service.cloudrun_service[count.index].status[0].url}/tensorflow.serving.PredictionService/Predict\"" : "httpRequest.status=200 httpRequest.requestUrl=\"${google_cloud_run_service.cloudrun_service[count.index].status[0].url}/v1/models/${var.model_name}:predict\""
#   depends_on             = [google_bigquery_table.dataset-table]
#   unique_writer_identity = true
# }

# resource "google_logging_project_sink" "logging_sink" {
#   count       = length(var.APIS)
#   name        = "${var.prefix}-${var.model_name}-${var.APIS[count.index]}-sink"
#   destination = "bigquery.googleapis.com/projects/${var.project_name}/datasets/${var.prefix}_${var.model_name}"

#   filter                 = var.APIS[count.index] == "grpc" ? "httpRequest.status=200 httpRequest.requestUrl=\"${google_cloud_run_service.cloudrun_service[count.index].status[0].url}/tensorflow.serving.PredictionService/Predict\"" : "httpRequest.status=200 httpRequest.requestUrl=\"${google_cloud_run_service.cloudrun_service[count.index].status[0].url}/v1/models/${var.model_name}:predict\""
#   unique_writer_identity = true
# }
