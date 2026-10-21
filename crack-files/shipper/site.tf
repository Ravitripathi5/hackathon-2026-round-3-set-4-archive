resource "aws_s3_bucket" "preview" {
  bucket = "log-archive-preview"
  acl    = "public-read"
}
