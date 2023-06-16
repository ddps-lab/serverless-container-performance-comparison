data "aws_sagemaker_prebuilt_ecr_image" "tensorflow-inference" {
  repository_name = "tensorflow-inference"
  image_tag = "2.11.1-cpu-py39-ubuntu20.04-sagemaker"
}