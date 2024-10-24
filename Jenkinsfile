pipeline {
    agent any
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['beta', 'production'], description: 'Choose environment')
        string(name: 'BRANCH', defaultValue: 'wip/feature/*', description: 'Enter branch')
        choice(name: 'SONAR_TEST', choices: ['Yes', 'No'], description: 'Do you want to enable Sonar test?')
    }
    stages {
        stage('Build') {
            steps {
                script {
                    // Build code here, e.g., using Docker
                    sh 'docker build -t my-app:${env.BRANCH} .'
                }
            }
        }
        stage('SonarQube Analysis') {
            when {
                expression { params.SONAR_TEST == 'Yes' }
            }
            steps {
                script {
                    // Add SonarQube analysis command here
                    sh 'sonar-scanner -Dsonar.projectKey=my-app -Dsonar.sources=. -Dsonar.host.url=http://your-sonarqube-url'
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    // Authenticate to ECR
                    withCredentials([[$class: 'AmazonWebServicesCredentials', credentialsId: 'aws-credentials']]) {
                        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your_account_id>.dkr.ecr.us-east-1.amazonaws.com'
                        // Tag and push image to ECR
                        sh 'docker tag my-app:${env.BRANCH} <your_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-app:${env.BRANCH}'
                        sh 'docker push <your_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-app:${env.BRANCH}'
                    }
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    // Deploy to EKS
                    withCredentials([[$class: 'AmazonWebServicesCredentials', credentialsId: 'aws-credentials']]) {
                        def clusterName = params.ENVIRONMENT == 'beta' ? 'my-beta-cluster' : 'my-production-cluster'
                        sh "kubectl set image deployment/my-app my-app=<your_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-app:${env.BRANCH} --context ${clusterName}"
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs() // Clean workspace after the build
        }
    }
}
