pipeline {
    // Run this on the dedicated agent we configured earlier
    agent { 
        label 'linux-docker' 
    }
    
    environment {
        // GCP Registry Configuration
        REGION     = 'asia-east1'
        PROJECT_ID = 'platypus-lab01'
        REPO_NAME  = 'otel-repo'
        APP_NAME   = 'simple-febedb-app'
        
        // Dynamically build the full registry path
        REGISTRY   = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        FULL_IMAGE = "${REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Uses the GitHub token we saved in Jenkins
                git branch: 'main', 
                    credentialsId: 'github-token', 
                    url: 'https://github.com/tribagus6/simple-febedb-app.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building image: ${FULL_IMAGE}"
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }
        
        stage('Authenticate & Push to GAR') {
            steps {
                // Securely inject the GCP JSON key into the workspace
                withCredentials([file(credentialsId: 'gcp-gar-key', variable: 'GCP_KEY')]) {
                    // Login to Artifact Registry using the JSON key
                    sh 'cat $GCP_KEY | docker login -u _json_key --password-stdin https://${REGION}-docker.pkg.dev'
                    
                    // Push the built image
                    echo "Pushing image to Artifact Registry..."
                    sh "docker push ${FULL_IMAGE}"
                }
            }
        }
    }
    
    post {
        always {
            // Clean up the local Docker daemon to save disk space on the VM
            sh "docker rmi ${FULL_IMAGE} || true"
            // Log out of the registry
            sh "docker logout https://${REGION}-docker.pkg.dev || true"
        }
    }
}
