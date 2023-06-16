
data "aws_iam_policy_document" "sagemaker-assume-role" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "sagemaker-role" {
  name               = "${var.prefix}-scpc-sagemaker-role"
  assume_role_policy = data.aws_iam_policy_document.sagemaker-assume-role.json
}

resource "aws_iam_role_policy_attachment" "sagemaker-full-access-policy" {
  role       = aws_iam_role.sagemaker-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "cloudwatch-full-access-policy" {
  role       = aws_iam_role.sagemaker-role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_role_policy_attachment" "cloudwatch-event-full-access-policy" {
  role       = aws_iam_role.sagemaker-role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchEventsFullAccess"
}

resource "aws_iam_role_policy_attachment" "cloudwatch-logs-full-access-policy" {
  role       = aws_iam_role.sagemaker-role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_role_policy_attachment" "s3-full-access-policy" {
  role       = aws_iam_role.sagemaker-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
