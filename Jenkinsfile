pipeline {
  agent {
    // Option A: run inside amazon/aws-cli docker image (recommended if agents don't have awscli)
    // docker { image 'amazon/aws-cli' }
    // Option B: use a normal agent that already has awscli installed
    label 'linux && awscli'
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
    timestamps()
  }

  environment {
    BUCKET = 'autoscorchdownload.com'
    AWS_REGION = 'eu-west-2'
    PROGRAM = 'scorch'
    CREDENTIALS_ID = 'aws-creds' // change to your Jenkins credential id
  }

  parameters {
    booleanParam(
      name: 'doClean',
      defaultValue: true,
      description: 'Clean workspace before build'
    )
  }

  stages {
    stage('Checkout master') {
      steps {
        // If the job is configured to build master (Pipeline script from SCM),
        // this will re-checkout the same repo/branch that loaded the Jenkinsfile.
        checkout scm
      }
    }

    // stage('Prepare & Package') {
    //   steps {
    //     sh '''
    //       set -euo pipefail
    //       str_ProgramName=${PROGRAM}
    //       str_ProgramVersion=$(grep -a "^typeset str_ProgramVersion=" ${str_ProgramName} | cut -d"=" -f2 | tr -d '"')
    //       echo "Program: ${str_ProgramName} Version: ${str_ProgramVersion}"
    //       ls -l
    //       tar cf scorch.tar ${str_ProgramName} bin obrar python functions plugins/DEMO
    //       ls -lR
    //       md5sum scorch.tar > scorch.tar.md5
    //       sha256sum scorch.tar > scorch.tar.sha256
    //       cp scorch.tar        escorch.${str_ProgramVersion}.tar
    //       cp scorch.tar.md5    escorch.${str_ProgramVersion}.tar.md5.txt
    //       cp scorch.tar.sha256 escorch.${str_ProgramVersion}.tar.sha256.txt
    //       echo ${str_ProgramVersion} > version.txt
    //       mv scorch.tar        latest.tar
    //       mv scorch.tar.md5    latest.tar.md5
    //       mv scorch.tar.sha256 latest.tar.sha256
    //       mv bin/install       install
    //       ls -l
    //     '''
    //   }
    // }

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


  //   stage('Upload to S3') {
  //     steps {
  //       // Use AWS Credentials plugin binding to set AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY
  //       withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: "${CREDENTIALS_ID}"]]) {
  //         sh '''
  //           set -euo pipefail
  //           export AWS_DEFAULT_REGION=${AWS_REGION}
  //           # Upload versioned artifacts
  //           aws s3 cp escorch.${str_ProgramVersion}.tar s3://${BUCKET}/ --acl public-read
  //           aws s3 cp escorch.${str_ProgramVersion}.tar.md5.txt s3://${BUCKET}/ --acl public-read
  //           aws s3 cp escorch.${str_ProgramVersion}.tar.sha256.txt s3://${BUCKET}/ --acl public-read
  //           # Upload latest copies
  //           aws s3 cp latest.tar s3://${BUCKET}/ --acl public-read
  //           aws s3 cp latest.tar.md5 s3://${BUCKET}/ --acl public-read
  //           aws s3 cp latest.tar.sha256 s3://${BUCKET}/ --acl public-read
  //           # Upload install and version
  //           aws s3 cp install s3://${BUCKET}/ --acl public-read
  //           aws s3 cp version.txt s3://${BUCKET}/ --acl public-read
  //         '''
  //       }
  //     }
  //   }
  // }

  post {
    success { echo "Pipeline finished: artifacts uploaded to s3://${BUCKET}/" }
    failure { echo "Pipeline failed — check console output." }
  }
}

