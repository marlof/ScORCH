pipeline {
  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '15', artifactNumToKeepStr: '5'))
    timestamps()
  }

  parameters {
    booleanParam(
      name: 'doClean',
      defaultValue: true,
      description: 'Clean workspace before build'
    )
  }

  stages {

    stage('Clean') {
      when {
        expression { params.doClean }
      }
      steps {
        cleanWs()
      }
    }

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup') {
      steps {
        script {

          // Identify environment target based on branch
          if (env.GIT_BRANCH == 'develop' || env.GIT_BRANCH ==~ /.*feature-.+/) {
            target    = 'dev'
            BuildType = '-dev'
          }
          else if (env.GIT_BRANCH ==~ /.*release-.+/) {
            target    = 'pre'
            BuildType = '-RC'
          }
          else if (env.GIT_BRANCH in ['master','main']) {
            target    = 'prod'
            BuildType = ''
          }
          else {
            error "Unknown branch type: ${env.GIT_BRANCH}. Expected develop/feature-/release-/master/main"
          }

          // Extract version from scorch script
          oversion = sh(
            script: "./scorch -v | cut -d '[' -f2 | tr -d ']'",
            returnStdout: true
          ).trim()

          shortver    = oversion.take(10)
          version     = "${shortver}-${env.BUILD_NUMBER}"

          prjname     = 'scorch'
          iacname     = env.JOB_NAME
          packagename = "${iacname}-v${version}.tar.gz"
          publish_url = "${env.NEXUS_URL}/repository/${prjname}/${packagename}"

          echo "INFO: Target: ${target}"
          echo "INFO: Version: ${version}"
          echo "INFO: Publish URL: ${publish_url}"
        }
      }
    }

    stage('Build') {
      steps {
        script {
          tagversion = sh(
            script: """
              git -c 'versionsort.suffix=-' \
                  ls-remote --exit-code --refs --sort='version:refname' --tags \
                  | tail --lines=1 \
                  | cut --delimiter="/" --fields=3
            """,
            returnStdout: true
          ).trim() + BuildType

          echo "INFO: Latest Tag: ${tagversion}"
          echo "INFO: Building ${prjname} from ${target} branch"
          echo "INFO: Build number: ${BUILD_NUMBER}"

          // Prepare build
          sh "mkdir -p ${prjname}-${BUILD_NUMBER}"

          // Update BUILDTAG in scorch file
          sh """
            sed -i "s/^BUILDTAG=.*/BUILDTAG=${tagversion}/" scorch
          """

          sh "mkdir -p plugins ; chmod 775 plugins"
          sh "ls -l"

          // Create tarball
          sh """
            tar cf ${prjname}-${tagversion}.tar \
              LICENSE README.md scorch obrar bin python functions plugins projects/common
          """
          sh "sha256sum ${prjname}-${tagversion}.tar > ${prjname}-${tagversion}.tar.sha256"
          sh "md5sum    ${prjname}-${tagversion}.tar > ${prjname}-${tagversion}.tar.md5"
        }
      }
    }

    stage('CI Unit Test') {
      when {
        expression { target == 'dev' }
      }
      steps {
        script {
          echo "INFO: Running DEV CI checks..."
          echo "INFO: Testing archive ${prjname}-${tagversion}.tar"

          sh "ls -l ${prjname}-${tagversion}.tar"

          dir("${prjname}-${BUILD_NUMBER}") {
            sh "tar xf ../${prjname}-${tagversion}.tar"
            sh "./scorch -h"
            sh "./scorch -v"
          }
        }
      }
    }

    stage('Approval (Production Only)') {
      when {
        expression { target == 'prod' }
      }
      steps {
        timeout(time: 30, unit: 'MINUTES') {
          input message: "Deploy to Production?", id: 'approval'
        }
      }
    }
  }

  post {
    always {
      sh "df -h"
      archiveArtifacts artifacts: '*.tar, *.sha256, *.md5', followSymlinks: false
    }
  }
}
