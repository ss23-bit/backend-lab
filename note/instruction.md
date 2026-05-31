provider "aws" → connect to Amazon Web Services in ap-southeast-1

data "aws_ami" → “find the latest matching AMI”

resource "aws_instance" → “I want an EC2 instance”
  - when we create instance AWS gives it: Public IP, Public DNS

(known after apply) → AWS will generate these values, Terraform doesn’t know them yet, after creation → they go into state

terraform fmt → Readable
terraform validate → Checks if your code is valid Terraform, catches missing arguments, wrong structure
terraform plan → Compares your code vs real AWS, shows EXACT changes

😌 *Why modern CI/CD is better than Jenkins*
No server to manage
No plugin hell
Runs in clean environments every time
Easy to read (YAML > Groovy)

1. Infrastructure
Jenkins: “You manage the CI system”
Modern: “CI system is managed for you

2. Execution model
Jenkins: long-running server, stateful
Modern: ephemeral runners (fresh every run), stateless

3. Scalability
Jenkins: manual scaling
Modern: auto scaling

4. Security
Jenkins: you patch it, you secure it
Modern: platform handles most of it

⚠️ **Real-world migration issues**
1. Environment differences
Jenkins: long-lived machine
GitHub Actions: fresh VM every run
👉 You must install everything each time

2. Hidden dependencies 
Jenkins might have: pre-installed Terraform, pre-installed Node
👉 You must explicitly add setup steps

3. State handling (Terraform)
If using Terraform:
👉 You SHOULD use remote state (e.g., S3)
Otherwise:
pipeline will break or recreate resources

Take EXISTING infrastructure → bring it into Terraform: `terraform import` When you already created the recources(eg.s3) in AWS console, you can't `apply` that if you want to put it on terraform, cause it already exist on AWS, we need to `import` and the terraform `state` will remember it

**Destroy Rules**
force_destroy = true 
---Or---
lifecycle {
  prevent_destroy = true
}

`Import` When used First time
`Drift` When used After already managed

`Drift`
🅰️ Accept reality (update code)
Update Terraform to match AWS then `terraform plan`

🅱️ Enforce Terraform (overwrite AWS)
Run: `terraform apply`
👉 Terraform will revert AWS back to your code