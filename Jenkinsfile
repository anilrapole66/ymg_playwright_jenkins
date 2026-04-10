/*
 * CI Pipeline — ymg_playwright_jenkins
 * ─────────────────────────────────────────────────────────────────────────────
 * Trigger : Every push to GitHub (via webhook)
 * Flow    : Clone → Setup → Migrate DB → Seed CI data → Run Playwright tests
 *           → (main only) Promote to stable branch
 *
 * Jenkins credentials required:
 *   DJANGO_SECRET_KEY  — Secret text
 *   PLAYWRIGHT_ADMIN   — Username with password  (TEST_ADMIN_USER / TEST_ADMIN_PASS)
 *   GITHUB_CREDENTIALS — Username with password  (GitHub username / Personal Access Token)
 *
 * GitHub webhook:
 *   Payload URL : http://<JENKINS_HOST>/github-webhook/
 *   Content type: application/json
 *   Events      : Just the push event
 */

pipeline {
    agent any

    options {
        timeout(time: 1, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        // Prevent two builds running simultaneously — both would try to bind port 8000
        disableConcurrentBuilds()
    }

    triggers {
        // Fires when GitHub sends a push webhook.
        // Requires the "GitHub Integration Plugin" installed in Jenkins.
        githubPush()
    }

    environment {
        REPO_URL      = 'https://github.com/anilrapole66/ymg_playwright_jenkins.git'
        PORTAL_DIR    = "${WORKSPACE}\\ymgportal"
        E2E_DIR       = "${WORKSPACE}\\playwright-learning"
        VENV_DIR      = "${WORKSPACE}\\venv"
        STABLE_BRANCH = 'stable'
    }

    stages {

        // ── 1. Source ──────────────────────────────────────────────────────────
        stage('Clone Repository') {
            options { timeout(time: 5, unit: 'MINUTES') }
            steps {
                // credentialsId is needed so Jenkins can push back later
                git branch: 'main',
                    credentialsId: 'GITHUB_CREDENTIALS',
                    url: "${REPO_URL}"
            }
        }

        // ── 2. Python env ─────────────────────────────────────────────────────
        stage('Setup Python / Django') {
            options { timeout(time: 10, unit: 'MINUTES') }
            steps {
                bat """
                    python -m venv ${VENV_DIR}
                    call ${VENV_DIR}\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r ${PORTAL_DIR}\\requirements.txt
                """
            }
        }

        // ── 3. DB ─────────────────────────────────────────────────────────────
        stage('Run Django Migrations') {
            options { timeout(time: 5, unit: 'MINUTES') }
            steps {
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY', variable: 'SECRET_KEY')]) {
                    bat """
                        call ${VENV_DIR}\\Scripts\\activate
                        cd ${PORTAL_DIR}
                        set PYTHONPATH=${PORTAL_DIR}
                        set DJANGO_SETTINGS_MODULE=employee_portal.settings_ci
                        set SECRET_KEY=%SECRET_KEY%
                        python manage.py migrate --run-syncdb
                    """
                }
            }
        }

        // ── 4. Seed ───────────────────────────────────────────────────────────
        // Creates the superuser and lookup data (MainClient, RoleSow) that
        // Playwright tests depend on. Idempotent — safe to run every build.
        stage('Seed CI Test Data') {
            options { timeout(time: 3, unit: 'MINUTES') }
            steps {
                withCredentials([
                    string(credentialsId: 'DJANGO_SECRET_KEY', variable: 'SECRET_KEY'),
                    usernamePassword(
                        credentialsId: 'PLAYWRIGHT_ADMIN',
                        usernameVariable: 'TEST_ADMIN_USER',
                        passwordVariable: 'TEST_ADMIN_PASS'
                    )
                ]) {
                    bat """
                        call ${VENV_DIR}\\Scripts\\activate
                        cd ${PORTAL_DIR}
                        set PYTHONPATH=${PORTAL_DIR}
                        set DJANGO_SETTINGS_MODULE=employee_portal.settings_ci
                        set SECRET_KEY=%SECRET_KEY%
                        set TEST_ADMIN_USER=%TEST_ADMIN_USER%
                        set TEST_ADMIN_PASS=%TEST_ADMIN_PASS%
                        python manage.py seed_ci
                    """
                }
            }
        }

        // ── 5. Playwright env ─────────────────────────────────────────────────
        stage('Setup Playwright') {
            options { timeout(time: 10, unit: 'MINUTES') }
            steps {
                dir("${E2E_DIR}") {
                    bat '''
                        npm ci
                        npx playwright install chromium --with-deps
                    '''
                }
            }
        }

        // ── 6. Tests ──────────────────────────────────────────────────────────
        // playwright.config.js webServer block starts Django automatically.
        // globalSetup logs in once and saves auth state before tests begin.
        stage('Run Playwright Tests') {
            options { timeout(time: 30, unit: 'MINUTES') }
            steps {
                withCredentials([
                    string(credentialsId: 'DJANGO_SECRET_KEY', variable: 'SECRET_KEY'),
                    usernamePassword(
                        credentialsId: 'PLAYWRIGHT_ADMIN',
                        usernameVariable: 'TEST_ADMIN_USER',
                        passwordVariable: 'TEST_ADMIN_PASS'
                    )
                ]) {
                    dir("${E2E_DIR}") {
                        bat """
                            set PATH=${VENV_DIR}\\Scripts;%PATH%
                            set CI=true
                            set PYTHONPATH=${PORTAL_DIR}
                            set DJANGO_SETTINGS_MODULE=employee_portal.settings_ci
                            set SECRET_KEY=%SECRET_KEY%
                            set TEST_ADMIN_USER=%TEST_ADMIN_USER%
                            set TEST_ADMIN_PASS=%TEST_ADMIN_PASS%
                            npx playwright test
                        """
                    }
                }
            }
        }

        // ── 7. Promote ────────────────────────────────────────────────────────
        // Only runs when all tests pass AND the push was to 'main'.
        // Pushes the current HEAD to the 'stable' branch — a branch that
        // always points to the last fully-tested commit.
        stage('Promote to Stable') {
            when {
                // env.GIT_BRANCH is set by the git step above
                expression { env.GIT_BRANCH ==~ /.*main/ }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'GITHUB_CREDENTIALS',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    bat """
                        git config user.email "jenkins@ci.local"
                        git config user.name "Jenkins CI"
                        git push https://%GIT_USER%:%GIT_TOKEN%@github.com/anilrapole66/ymg_playwright_jenkins.git HEAD:refs/heads/${STABLE_BRANCH} --force
                    """
                }
                echo "Promoted build #${env.BUILD_NUMBER} to '${STABLE_BRANCH}' branch."
            }
        }
    }

    // ── Post ──────────────────────────────────────────────────────────────────
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
            mail(
                to: 'team@example.com',
                subject: "Build Passed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "All tests passed on '${env.GIT_BRANCH}'.\nReport: ${env.BUILD_URL}Playwright_Test_Report"
            )
        }

        failure {
            mail(
                to: 'team@example.com',
                subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Tests failed on '${env.GIT_BRANCH}'.\nReport: ${env.BUILD_URL}Playwright_Test_Report"
            )
        }
    }
}
