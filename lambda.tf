module "google_download_pdf" {
  source         = "terraform-aws-modules/lambda/aws"
  function_name  = "google-translate-pdf"
  create_package = false
  image_uri      = module.docker_image.image_uri
  package_type   = "Image"
  architectures  = ["x86_64"]
  timeout        = 180
  memory_size    = 1024
  hash_extra     = "google_translate_pdf"
}

module "docker_image" {
  source          = "terraform-aws-modules/lambda/aws//modules/docker-build"
  create_ecr_repo = true
  ecr_repo        = "google-translate-pdf"
  image_tag       = filesha1("${path.module}/utils.py")
  source_path     = path.module
  platform        = "linux/amd64"

  ecr_repo_lifecycle_policy = jsonencode({
    "rules" : [
      {
        "rulePriority" : 1,
        "description" : "Keep only the last 2 images",
        "selection" : {
          "tagStatus" : "any",
          "countType" : "imageCountMoreThan",
          "countNumber" : 2
        },
        "action" : {
          "type" : "expire"
        }
      }
    ]
  })
}
