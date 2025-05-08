pipeline{
    agent any
    stages {
        stage('version') {
            steps {
                echo 'Building...'
                sh 'python3 --version'
            }
        }
        stage('install packages') {
            steps {
                echo 'Environment setup...'
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Deploying...'
                sh '. .venv/bin/activate && pytest test.py'
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                echo 'Building Docker image...'
                withCredentials([string(credentialsId: 'docker-hub-credentials-id', variable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u mhfahad --password-stdin'
                }
                sh 'docker build -t mhfahad/fastapi-cicd:latest -f ./Dockerfile .'
                echo 'Pushing Docker image to Docker Hub...'
                sh 'docker push mhfahad/fastapi-cicd:latest'
            }
        }
    }
}