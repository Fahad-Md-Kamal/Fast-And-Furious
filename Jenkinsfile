pipeline {
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
                withCredentials([
                    string(credentialsId: 'docker-hub-credentials-id', variable: 'DOCKER_PASSWORD'),
                    string(credentialsId: 'docker-hub-username-id', variable: 'DOCKER_USERNAME')
                ]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker build -t $DOCKER_USERNAME/fastapi-cicd:latest -f ./Dockerfile .'
                    echo 'Pushing Docker image to Docker Hub...'
                    sh 'docker push $DOCKER_USERNAME/fastapi-cicd:latest'
                }
            }
        }
    }
    post {
        always {
            echo 'Sending Slack notification...'
            withCredentials([string(credentialsId: 'SLACK_CHANNEL', variable: 'SLACK_CHANNEL')]) {
                slackSend(
                    channel: env.SLACK_CHANNEL,
                    color: currentBuild.result == 'SUCCESS' ? 'good' : 'danger',
                    message: "Build ${currentBuild.fullDisplayName} finished with status: ${currentBuild.result}"
                )
            }
        }
    }
}