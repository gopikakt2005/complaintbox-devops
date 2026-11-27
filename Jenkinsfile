pipeline {
    agent any

    stages {
        stage('Django Validation') {
            steps {
                sh '''
                docker run --rm -v "$WORKSPACE:/app" -w /app python:3.10-slim sh -c "pip install -r requirements.txt && python manage.py check --settings=dast_settings"
                '''
            }
        }

        stage('SAST - Semgrep') {
            steps {
                sh '''
                docker run --rm -v "$WORKSPACE:/src" -w /src semgrep/semgrep semgrep scan --config auto --json --output sast-report.json /src
                '''
            }
        }

        stage('Dependency Scan') {
            steps {
                sh '''
                docker run --rm -v "$WORKSPACE:/src" -w /src python:3.10-slim sh -c "pip install pip-audit && pip-audit -r requirements.txt -f json -o dependency-report.json || true"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t complaintbox:${BUILD_NUMBER} .'
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                sh '''
                docker rm -f complaintbox-dast-${BUILD_NUMBER} 2>/dev/null || true
                docker run -d --name complaintbox-dast-${BUILD_NUMBER} -p 18000:8000 complaintbox:${BUILD_NUMBER}
                sleep 15
                docker run --rm --network host -v "$WORKSPACE:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://127.0.0.1:18000 -r dast-report.html || echo "ZAP completed with warnings; review the report."
                docker rm -f complaintbox-dast-${BUILD_NUMBER} || true
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*-report.*', allowEmptyArchive: true
            sh 'docker rm -f complaintbox-dast-${BUILD_NUMBER} 2>/dev/null || true'
        }
    }
}
