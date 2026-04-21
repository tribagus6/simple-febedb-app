pipeline {
    agent { 
        label 'linux-docker' 
    }
    
    environment {
        REGION     = 'asia-east1'
        PROJECT_ID = 'platypus-lab01'
        REPO_NAME  = 'otel-repo'
        APP_NAME   = 'simple-febedb-app'
        
        REGISTRY   = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    credentialsId: 'tribagus6-github-pat', 
                    url: 'https://github.com/tribagus6/simple-febedb-app.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building image: ${FULL_IMAGE}"
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }
        
        stage('Keyless Authenticate & Push') {
            steps {
                // The 'sh' block runs on the Jenkins Agent container.
                // Because the container is on the VM, it can hit the internal metadata IP.
                sh '''
                    echo "Fetching dynamic access token from GCP Metadata Server..."
                    
                    # 1. Ask the VM for a short-lived OAuth token
                    TOKEN=$(curl -s -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" | grep -o '"access_token":"[^"]*"' | awk -F'"' '{print $4}')
                    
                    # 2. Use the token to log into Artifact Registry
                    # We use the special username 'oauth2accesstoken' for this method
                    echo $TOKEN | docker login -u oauth2accesstoken --password-stdin https://${REGION}-docker.pkg.dev
                    
                    # 3. Push the image
                    echo "Pushing image to Artifact Registry..."
                    docker push ${FULL_IMAGE}
                '''
            }
        }
    }
    
    post {
        always {
            sh "docker rmi ${FULL_IMAGE} || true"
            sh "docker logout https://${REGION}-docker.pkg.dev || true"
        }
    }
}
