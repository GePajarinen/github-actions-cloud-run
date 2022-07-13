# Github actions (Cloud Run)   

Create your directory in github and add all your application.    
In this case, my directory is called RUN and inside it I have two files:  
   - main.py   
   - Dockerfile   

Go to **Settings**:   
![image](https://user-images.githubusercontent.com/58811514/178796626-ca3de7e5-f12c-4928-8f49-91671f8b847a.png)   

Then, to **Secrets** > **Actions**:   
![image](https://user-images.githubusercontent.com/58811514/178797012-4c1763ed-5ef8-4ad3-b7a0-9d7885750d79.png)   

New repository secret:   
![image](https://user-images.githubusercontent.com/58811514/178797174-6fa73b1b-2997-4809-a3ad-d59e8a85ecf6.png)    

**Name:** GCP_PROJECT   
**Value:** #Your project id   
**Add secret**   

Repeat the process for GCP_SA_EMAIL and GCP_SA_KEY:   

**Name:** GCP_SA_EMAIL   
**Value:** #The service account from GCP that is going to use the github actions   
**Add secret**   

**Name:** GCP_SA_KEY   
**Value:** #The key of the service account.   
**Add secret**   

PS.: You can create a special service account to be responsible only for managing the github actions.   
To create a service account and get the key, check here. (add the link)   

Create another directory called: .github/workflows   
Inside, create a .yaml file (I called my teste.yaml) and write in it the configuration:   
```yaml
on:
    push:
        branches:
            - main

name: Demos 1 - Build and Deploy

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout
          uses: actions/checkout@v2
          
        - name: Setup Cloud SDK
          uses: google-github-actions/setup-gcloud@v0.2.0
          with:
            project_id: ${{ secrets.GCP_PROJECT }}
            service_account_key: ${{ secrets.GCP_SA_KEY }}
            export_default_credentials: true
            
        - name: Authorize Docker push
          run: gcloud auth configure-docker

        - name: Build and Push Container
          run: |-
            #docker build -t --tag=gcr.io/${{ secrets.GCP_PROJECT }}/gkeapp:${{ github.she }} .
            #docker push gcr.io/${{ secrets.GCP_PROJECT }}/gkeapp:${{ github.sha }}
            gcloud builds submit gke --tag=gcr.io/${{ secrets.GCP_PROJECT }}/gkeapp:${{ github.sha }}
            
        - name: Deploy to Cloud Run
          id: deploy
          uses: google-github-actions/deploy-cloudrun@v0.2.0
          with:
                service: gke-service
                image: gcr.io/${{ secrets.GCP_PROJECT }}/gkeapp:${{ github.sha }}
                #env_vars: TITLE=Demo 1, SECRET=${{ secrets.SECRET_NAME }}
                
        - name: Show Output
          run: echo ${{ steps.deploy.outputs.url }}
```

When you commit the .yaml, the process will start:


