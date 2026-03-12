pipeline {
    agent any

    environment {
        REPO_URL   = 'https://github.com/anilrapole66/ymg_playwright_jenkins.git'
        PORTAL_DIR = "${WORKSPACE}\\ymgportal"
        E2E_DIR    = "${WORKSPACE}\\playwright-learning"
        VENV_DIR   = "${WORKSPACE}\\venv"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: "${REPO_URL}"
            }
        }

        stage('Setup Python / Django') {
            steps {
                bat '''
                    python -m venv %WORKSPACE%\\venv
                    call %WORKSPACE%\\venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r %WORKSPACE%\\ymgportal\\requirements.txt
                '''
            }
        }

        stage('Run Django Migrations (CI DB)') {
            steps {
                bat '''
                    call %WORKSPACE%\\venv\\Scripts\\activate
                    cd %WORKSPACE%\\ymgportal
                    set DJANGO_SETTINGS_MODULE=employee_portal.settings_ci
                    python manage.py migrate --run-syncdb
                '''
            }
        }

        stage('Setup Playwright') {
            steps {
                dir("${E2E_DIR}") {
                    bat '''
                        npm ci
                        npx playwright install chromium --with-deps
                    '''
                }
            }
        }

        stage('Run Playwright Tests') {
            steps {
                dir("${E2E_DIR}") {
                    bat '''
                        set PATH=%WORKSPACE%\\venv\\Scripts;%PATH%
                        set CI=true
                        set DJANGO_SETTINGS_MODULE=employee_portal.settings_ci
                        npx playwright test
                    '''
                }
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'playwright-learning/playwright-report',
                reportFiles: 'index.html',
                reportName: 'Playwright Test Report'
            ])

            junit(
                testResults: 'playwright-learning/test-results/junit-report.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'playwright-learning/test-results/**/*',
                allowEmptyArchive: true
            )
        }

        success {
            echo '✅ All Playwright tests passed!'
        }

        failure {
            echo '❌ Tests failed — check Playwright Report above'
        }
    }
}
