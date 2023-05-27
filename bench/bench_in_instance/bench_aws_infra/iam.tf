data "aws_iam_policy_document" "ec2-service-for-iam-role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "bench-instance-role" {
  name               = "${var.prefix}-bench-instance-role"
  assume_role_policy = data.aws_iam_policy_document.ec2-service-for-iam-role.json
}

resource "aws_iam_role_policy_attachment" "bench-instance-role-attach-ssm-policy" {
  role       = aws_iam_role.bench-instance-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "bench-instance-role-attach-s3-full-access" {
  role       = aws_iam_role.bench-instance-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "bench-instance-role-attach-ecr-full-access" {
  role       = aws_iam_role.bench-instance-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
}

resource "aws_iam_role_policy_attachment" "bench-instance-role-attach-cloudwatch-logs-full-access" {
  role       = aws_iam_role.bench-instance-role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_instance_profile" "bench-instance-role-instance-profile" {
  name = "${var.prefix}-bench-instance-role-instnace-profile"
  role = aws_iam_role.bench-instance-role.name
}
