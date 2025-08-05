.PHONY: init plan apply destroy

init:
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform init \
		-reconfigure \
		-backend-config="bucket=terraform_statefiles_nishantlabs" \
		-backend-config="prefix=ragfolio" 

fmt:
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform fmt

check:
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform validate
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform fmt -check

plan:
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform plan

apply:
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform apply -auto-approve
destroy:
	@GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json" \
		terraform destroy -auto-approve
