# Variables
$VM_INSTANCE = "instance-20240512-155200"
$VM_ZONE = "europe-north1-a"
$PROJECT_ID = "interview-bot-423115"

$VM_PROJECT_DIR = "~/interview-bot-site"


# SSH into the VM and execute commands
gcloud compute ssh $VM_INSTANCE --zone $VM_ZONE --project $PROJECT_ID --command="
    cd $VM_PROJECT_DIR &&
    git pull origin master
"

# wait so the message below is properly diplayed
Start-Sleep -Seconds 1

if ($? -eq $True) {
    Write-Host "Deployed"
} else {
    Write-Host "Deployment failed"
}